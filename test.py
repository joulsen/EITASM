#!/usr/bin/python

import argparse
import sys
import re
import json

OPCODES = json.load(open("opcodes.json"))
file = open("examples/quickmaths.asm")
program = file.read()

def get_intermediate_opcode(reference):
    return OPCODES[reference]["i_version"]

def expound_intermediate(program):
    new_program = ""
    for line in program.split('\n'):
        if '$' in line:
            operator = line.split(' ')[0]
            sibling = get_intermediate_opcode(operator)
            line = line.replace(operator, sibling)
            line = line.replace('$', '')
        new_program += line + '\n'
    return new_program.strip()

def expound_types(program):
    new_program = ""
    for line in program.split('\n'):
        if not line.endswith(':'):
            opcode = line.split(' ')[0]
            if OPCODES[opcode]["type"] is 'rv':
                pass
            elif OPCODES[opcode]["type"] is 'r':
                print(line)
                line += " 0"
            elif OPCODES[opcode]["type"] is 'v':
                words = line.split(' ')
                print(line)
                line += " 0"
            new_program += line + '\n'
    return new_program.strip()


def unify_words(program):
    new_program = ""
    for line in program.split('\n'):
        for word in line.split(' '):
            if word.startswith("0x"):
                new_program += str(int(word, 16))
            elif word.startswith("0b"):
                new_program += str(int(word, 2))
            elif word.isdigit():
                new_program += str(int(word))
            else:
                new_program += word
            new_program += ' '
        new_program += '\n'
    return new_program

def insert_bytecodes(program):
    for opcode, details in OPCODES.items():
        program = program.replace(opcode + ' ', str(details["bytecode"])+ ' ')
    return program

#def compact(program):
#    new_program = []
#    labels = {}
#    for i, line in enumerate(program.split('\n')):
#        if ':' in line:
#            labels[line.strip()[:-1]] = len(new_program)
#        else:
#            for word in line.split(' '):
#                if not word.isspace() and not word is '':
#                    new_program.append(word)
#
#    for i, word in enumerate(new_program):
#        if word in labels.keys():
#            new_program[i] = labels[word]
#    return list(map(int, new_program))

def clean(program):
    new_program = ""
    for i, line in enumerate(program.split('\n')):
        if (not line.isspace()) and (line != ''):
            new_program += line.strip() + '\n'
    return new_program

def replace_labels(program):
    new_program = ""
    pc = 0
    labels = {}
    for i, line in enumerate(program.split('\n')):
        if ':' in line:
            labels[line.strip()[:-1]] = pc
        else:
            new_program += line + '\n'
            pc += 1

    for label, value in labels.items():
        new_program = new_program.replace(label, str(value))
    return new_program.strip()

def combine(program):
    bytecode = []
    for line in program.split('\n'):
        nums = list(map(int, line.split(' ')))
        if len(nums) == 3:
            print("{:02X}{:01X}{:04X}".format(*nums))
        elif len(nums) == 2:
            print("{:02X}{:01X}{:04X}".format(*nums))

def code_to_vhdl(compact_program):
    prefix = 'signal PROG : ram_type := ('
    suffix = ', others => x"00");'

