import gdb

def calltrace_str(ct):
    acc = ""
    for i, frame in enumerate(ct):
        acc += ("  " * i) + frame + "\n"
    return acc

class CalltracePoint(gdb.Breakpoint):
    def __init__(self, spec):
        self.calltraces = []
        super(CalltracePoint, self).__init__(spec, gdb.BP_BREAKPOINT)
    def stop(self):
        print("in stop")
        calltrace = []
        frame = gdb.newest_frame()
        while frame is not None:
            sal = frame.find_sal()
            calltrace.append("%#x %s %s %d" % (frame.pc(), frame.function(),
                                               sal.symtab.filename, sal.line))
            frame = frame.older()

        calltrace.reverse()
        self.calltraces.append(calltrace)
        print("len(calltraces) = %d" % len(self.calltraces))
        return False
    def print_summary(self):
        print("got hit %d times" % len(self.calltraces))
        for ct in self.calltraces:
            print(calltrace_str(ct))

def exit_handler(bp, event):
    bp.print_summary()
    bp.delete()

class CalltracePointCommand(gdb.Command):
    def __init__(self):
        super(CalltracePointCommand, self).__init__("calltrace-point", gdb.COMMAND_OBSCURE, gdb.COMPLETE_LOCATION)
    def invoke(self, arg, from_tty):
        bp = CalltracePoint(arg)
        handler = lambda event: exit_handler(bp, event)
        gdb.events.exited.connect(handler)

CalltracePointCommand()
