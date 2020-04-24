// This program loops reg0 through 10-5
LOAD 1 $5

Loop1:
LOAD 0 $10

Loop2:
SUB 0 $1
SLEQ 0 1
GOTO Loop2
GOTO Loop1

