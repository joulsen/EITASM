// On Off setup
PUSH 0
SOMUX 0x0120  // Pin 1, ONOFF type, Instance 0
LOAD 0 $21    // REF = 21
OOCW 0 0x0500 // Register 0, Instance 0, REF Type, Useless nibbles x2
LOAD 0 $18    // Limit = 18
OOCW 0 0x0600 // Register 0, Instance 0, LIMIT Type
LOAD 0 $0     // Reverse = 0
OOCW 0 0x0700 // Register 0, Instance 0, REVERSE Type
CLRMEM 0x100
MSB 1 1
POP 0

// On Off main
PUSH 0
PUSH 1
OnOffStart:
SNRDY 1
GOTO ReadDetermine
GOTO OnOffEnd

ReadDetermine:
LOAD 0 0x100
SEQ 0 $0
GOTO ReadValue
GOTO ReadDelim

ReadDelim:
READ 0 1
SEQ 0 $35 // 35 = #
GOTO OnOffEnd
LOAD 0 $1
STORE 0 0x100
GOTO OnOffStart

ReadValue:
SEQ 0 $2
GOTO ReadValue1
READ 0 1
LOAD 1 0x101
CONC 0 1
OOCW 0 0x0400
CLRMEM 0x100
GOTO OnOffEnd

ReadValue1:
READ 0 1
STORE 0 0x101
LOAD 0 $2
STORE 0 0x100
GOTO OnOffStart

OnOffEnd:
POP 1
POP 0
