// This program is for testing the general functionality of the assembler
// It will feature labels, comments and many different opcodes.
Start:
ADD 0 $4

// The following loop will do reg0*4 until reg0 equals 4096
Loop_1:
MULU 0 $4
SEQi 0 0x1000 // 4096
GOTO Loop_1

SUB 0 $0b0001
ANDi 0 0xAA // 4095 AND 170 = 170
ADD 1 $0b11101101
OR 0 1 // 0b1010 1010 OR 0b1110 1101 = 1110 1111 = 0xEF
CLEAR 0
LOAD 1 $0 // Same as clear

ADDi 0 0xFF
ADD 5 $0xAA
Loop_with_a_very_long_label:
NOP
SUBi 0 1
SLESS 0 5 // Skips if reg0 < reg5
GOTO Loop_with_a_very_long_label
GOTO Start

