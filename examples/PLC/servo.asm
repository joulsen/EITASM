SOMUX 0x0010 // First nibble useless, Pin 0, PWM type, Instance 0
SPWM 0x0001 // Setup PWM 0, Set CMD = ENABLE, value = 1
SPWM 0x010B // PRESCALAR = 11
SPWM 0x039C // OVERFLOW = 156

Main:
SPWM 0x0290 // COMPARE = 144 (1.5 ms period = 0)

SEC 15
Delay1:
SEC 14
SUB 14 15
SEQ 14 $2
GOTO Delay1

SPWM 0x028C // COMPARE = 140 (2 ms period = 90)

SEC 15
Delay2:
SEC 14
SUB 14 15
SEQ 14 $2
GOTO Delay2

GOTO Main
