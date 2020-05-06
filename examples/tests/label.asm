// This program is for testing that similiar (but not equal) labels are inserted correctly.
A:
ADD 0 1
BB:
ADD 0 1
B:
// This is a line for testing purposes
ADD 0 1
A_B:
ADD 0 1
// This is a line for testing purposes
Wait:
ADD 0 1
// This is a line for testing purposes
// This is a line for testing purposes
Wait_for_something:
ADD 0 1
A_BCDEF:
// This is a line for testing purposes
ADD 0 1

GOTO Wait_for_something // Goto 5
GOTO A // Goto 0
GOTO BB // Goto 1
// This is a line for testing purposes
GOTO A_B // Goto 3
GOTO B // Goto 2
// This is a line for testing purposes
GOTO A_BCDEF // Goto 6
GOTO Wait // Goto 4
