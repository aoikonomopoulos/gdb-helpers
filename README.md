# GDB helpers

Random assortment of GDB helper scripts.

## calltrace-point

Collects calltraces every time the specified program point is reached, holds them in a tree and counts the number of hits. When the program ends, it will print out the tree. For example, a sample tree for a location in function `P` would look like:

```
A
 B
 +C
 | D
 | +E
 | | F
 | |  P (x hits)
 | +P (y hits)
 +G
   P (z hits)
```

The paths are presented in order of first appearence.

This command is useful to get a sense of how a piece of code is used in a large code base; simply do `caltrace-point <breakpoint spec>`, let the program run and read the calltraces to understand how the program point is reached in the execution scenario you care about.
