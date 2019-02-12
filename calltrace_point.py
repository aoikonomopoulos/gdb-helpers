import gdb

class TraceTree:
    def __init__(self):
        self.root = TraceTreeNode("")
    def add_trace(self, trace):
        curr_node = self.root
        for o in trace:
            child = curr_node.child(o)
            if child is None:
                child = TraceTreeNode(o)
                curr_node.add_child(child)
            else:
                child.hit()
            curr_node = child
            continue
    def to_s(self):
        if self.root is None:
            return "<empty>"
        return self.root.to_s("", -1)

class TraceTreeNode:
    def __init__(self, o):
        self.obj = o
        self.children = []
        self.hits = 1
    def add_child(self, o):
        if self.child(o) is not None: # we depend on an appropriate o.__eq__
            raise "BUG: tried to add duplicate child"
        self.children.append(o)
    def child(self, o):
        for ch in self.children:
            if o == ch.obj:
                return ch
    def hit(self):
        self.hits += 1
    def hits(self):
        return self.hits
    def to_s(self, acc, depth):
        # Negative depth means "skip this many levels". Used to
        # skip our dummy root node.
        if depth >= 0:
            acc += " " * depth + str(self.obj)
            if len(self.children) == 0:
                acc += " (#%d hits)\n" % self.hits
                return acc
            acc += "\n"
        for ch in self.children:
            acc = ch.to_s(acc, depth + 1)
        return acc


def calltrace_str(ct):
    acc = ""
    for i, frame in enumerate(ct):
        acc += ("  " * i) + frame + "\n"
    return acc

class CalltracePoint(gdb.Breakpoint):
    def __init__(self, spec):
        self.spec = spec
        self.calltraces = TraceTree()
        super(CalltracePoint, self).__init__(spec, gdb.BP_BREAKPOINT)
    def stop(self):
        calltrace = []
        frame = gdb.newest_frame()
        while frame is not None:
            filepath = "??"
            line = 0
            sal = frame.find_sal()
            if sal is not None:
                if sal.symtab is not None:
                    filepath = sal.symtab.filename
                line = sal.line
            calltrace.append("%#x %s %s:%d" % (frame.pc(), frame.function(),
                                               filepath, line))
            frame = frame.older()

        calltrace.reverse()
        self.calltraces.add_trace(calltrace)
        return False
    def print_summary(self):
        print("Call traces at %s" % self.spec)
        print(self.calltraces.to_s())
    def reset(self):
        self.calltraces = TraceTree()

def exit_handler(bp, event):
    bp.print_summary()
    bp.reset()

class CalltracePointCommand(gdb.Command):
    def __init__(self):
        super(CalltracePointCommand, self).__init__("calltrace-point", gdb.COMMAND_OBSCURE, gdb.COMPLETE_LOCATION)
    def invoke(self, arg, from_tty):
        bp = CalltracePoint(arg)
        handler = lambda event: exit_handler(bp, event)
        gdb.events.exited.connect(handler)

CalltracePointCommand()
