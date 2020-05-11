// The purpose of this test is to show that includes work.
// If no quotation marks are used, the assembler will look
// for a file in the /include/ folder.
// Both " and ' are accepted as quotes.
#include math
#include "nop.asm"

NOP

#include '../fibonacci.asm'

