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
        return self.root.to_s("", [], -1, True, False)

def print_node(branches, depth, only_sibling):
    # Branches are the points at which there is an "open"
    # branching point, i.e. the points where we need to
    # print out a '|' symbol
    branches = [br for br in branches if br > 0]
    acc = ""

    # We walk the branch points by increasing this index
    bridx = 0

    # Walk the columns from zero to our current depth
    for i in range(0, depth):
        if bridx == len(branches):
            # no pending branches
            acc += ' '
        elif i == branches[bridx]:
            # We're at a branching point
            if i == (depth - 1):
                if not only_sibling:
                    acc += '+'
                else:
                    acc += ' '
            else:
                acc += '|'
            bridx += 1
        else:
            acc += ' '
    return acc

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
    def to_s(self, acc, branches, depth, only_sibling, last_sibling):
        if depth >= 0:
            x = print_node(branches, depth, only_sibling) + str(self.obj)
            acc += x
            if len(self.children) == 0:
                acc += " (#%d hits)\n" % self.hits
                return acc
            acc += "\n"
        if last_sibling:
            branches.pop()
        # Each lower level should have us as a branching point,
        # except for the last child
        branches = branches.copy()
        # NOTE: the branch marks need to appear at (depth - 1)
        branches.append(depth)
        only_sibling = len(self.children) == 1
        for (ch_off, ch) in enumerate(self.children):
            last_sibling = ch_off == (len(self.children) - 1)
            acc = ch.to_s(acc, branches, depth + 1, only_sibling, last_sibling)
        return acc

if __name__ == "__main__":
    tt = TraceTree()

    tt.add_trace(["a", "b", "c", "d", "g", "x", "y"])
    tt.add_trace(["a", "b", "c", "d", "g", "w", "z"])
    tt.add_trace(["a", "b", "e", "f"])
    print(tt.to_s())
