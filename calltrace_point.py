import gdb
import os
from importlib.machinery import SourceFileLoader

tracetree = SourceFileLoader("tracetree", os.path.dirname(os.path.abspath(__file__)) + "/tracetree.py").load_module()

def calltrace_str(ct):
    acc = ""
    for i, frame in enumerate(ct):
        acc += ("  " * i) + frame + "\n"
    return acc

class CalltracePoint(gdb.Breakpoint):
    def __init__(self, spec):
        self.spec = spec
        self.calltraces = tracetree.TraceTree()
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
        self.calltraces = tracetree.TraceTree()

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
