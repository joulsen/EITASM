Setup:
SOMUX 0x0120  // Pin 1, ONOFF type, Instance 0
LOAD 0 $21    // REF = 21
OOCW 0 0x0500 // Register 0, Instance 0, REF Type, Useless nibbles x2
LOAD 0 $18    // Limit = 18
OOCW 0 0x0600 // Register 0, Instance 0, LIMIT Type
LOAD 0 $0     // Reverse = 0
OOCW 0 0x0700 // Register 0, Instance 0, REVERSE Type


LOAD 0 $15
LOAD 1 $0
LOAD 2 $15
LOAD 3 $25

Main:
OOCW 0 0x0400
SNEQ 1 $0
ADD 0 $1
SEQ 1 $0
SUB 0 $1

SNEQ 0 3
LOAD 1 $1
SNEQ 0 2
LOAD 1 $0

GOTO Main
