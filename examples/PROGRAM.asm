setup:

// setup GSM module
// msb first 
// setup baud rate
MSB 0 1 				// send msb first on port 0
LOAD 15 $0 				// retry counter
LOAD 14 $2				// compare value
GSM:
SNEQ 14 15
GOTO TimeOut
LOAD 0 $0x41 			// A
LOAD 1 $0x54 			// T
LOAD 2 $0x0D 			// <CR>
WRITE 0 0 				// send A
WRITE 1 0 				// send T
WRITE 2 0 				// send <CR>
ADD 15 $1 				// add one to retry counter


// wait for response from GSM
LOAD 11 $4 				// load 4 for compare
LOAD 10 $0 				// load 0 as counting variable
SEC 13 					// reference time in sec
response:
SEC 12					// check time
SEQ 12 13  				// break out if no response
GOTO GSM
SRDY 0					// skip if there are data on port 0
GOTO response
READ 0 0				// read byte from port 0
PUSH 0					// push data to stack
ADD 10 $1 				// increment byte counter
SEQ 10 11				// check loop condition
GOTO response


// check GSM reply
LOAD 0 $0x4F 			// O
LOAD 1 $0x4B 			// K
LOAD 2 $0x0D 			// <CR> (carriage return)
LOAD 3 $0x0A 			// <LF> (new line)
POP 7 					// read data from stack
POP 6
POP 5
POP 4
SEQ 0 4
GOTO GSM
SEQ 1 5
GOTO GSM
SEQ 2 6
GOTO GSM
SEQ 3 7
GOTO GSM


loop:
LOAD 0 $0x35			// 0011 0101
DWRITE 0
GOTO loop


TimeOut:
LOAD 0 $0xA3			// 1010 0011
DWRITE 0				// write output
GOTO TimeOut