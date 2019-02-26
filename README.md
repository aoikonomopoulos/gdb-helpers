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

This command is useful to get a sense of how a piece of code is used in a large code base; simply do `calltrace-point <breakpoint spec>`, let the program run and read the calltraces to understand how the program point is reached in the execution scenario you care about.

## License information

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
