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
// The onoff controller permanently uses 0 registers
// It uses the ram adresses 0x100 and 0x101.
onoff_main:
PUSH 0                    // First the used registers are pushed.
PUSH 1
onoff_start:
SNRDY 1                   // Only do something if data is ready.
GOTO onoff_read_determine
GOTO onoff_end

onoff_read_determine:
LOAD 0 0x100              // Here we determine what the program must do
SEQ 0 $0                  // If the state in ram 0x100 is 0 we must read delimiter
GOTO onoff_read_value
GOTO onoff_read_delim

onoff_read_delim:
READ 0 1                  // If the state is 0, we read the delimiter and alter state
SEQ 0 $35                 // 35 = #. The delimiter is a #
GOTO onoff_end
LOAD 0 $1
STORE 0 0x100
GOTO onoff_start

onoff_read_value:
SEQ 0 $2                  // Here we check state again
GOTO onoff_read_value1    // GOTO if state is 1
READ 1 1
LOAD 0 0x101              // We load the first part of the byte read in state 1
CONC 0 1                  // We concatenate the two bytes to get the full value
OOCW 0 0x0400             // The value is written to the onoff controller
CLRMEM 0x100              // The state is reset
GOTO onoff_end

onoff_read_value1:
READ 0 1                  // Here we read the first byte of 2 bytes of data from sensor input
STORE 0 0x101             // It is stored into ram 0x101
LOAD 0 $2
STORE 0 0x100
GOTO onoff_start

onoff_end:
POP 1
POP 0

