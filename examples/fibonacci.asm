// This program will create a sequence of fibannoci numbers on register 2
// The sequence is: 1,1,2,3,5,8,13,21,34,...
Start:
LOAD 0 $1
LOAD 1 $1

Loop:
MOV 2 0
ADD 0 1
SLEQ 1 0 // Overflow protection
GOTO Start
MOV 2 1
ADD 1 0
SLEQ 0 1 // Overflow protection
GOTO Start
GOTO Loop

