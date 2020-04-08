#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:15:02 2020

@author: Andreas
"""

import argparse
import sys
import re
import json

parser = argparse.ArgumentParser(description="Assembler for Supercigar's CPU")
parser.add_argument('input', metavar='I', 
                    help="Input file for assembly code",
                    type=argparse.FileType('r'), nargs=1)

parser.add_argument('output', metavar='O', type=argparse.FileType('w'),
                    help="Output file for VHDL code (leave blank for stdout)",
                    nargs='?', default=sys.stdout)

parser.add_argument('opcodes', metavar='--opcodes',
                    help="Specifies location of opcode JSON (default opcodes.json)",
                    type=argparse.FileType('r'), nargs='?', default="opcodes.json")

args = parser.parse_args()


OPCODES = json.load(args.opcodes)

label_finder = re.compile(r"([a-zA-Z]+):")


def convert_to_bytecode(stream):
    for key, value in OPCODES.items():
        stream = stream.replace(key, str(value))
    stream = stream.replace('\n', ' ')
    
    result = []
    labels = {}
    for i, word in enumerate(stream.split(' ')):
        if word.strip().endswith(':'):
            labels[word[:-1]] = i
        elif len(word) and not word.isspace():
            result.append(word)
    
    stream = " ".join(result)
    for key, value in labels.items():
        stream = stream.replace(key, str(value))
    try:
        result = list(map(int, stream.split(' ')))
    except ValueError:
        for i, word in enumerate(stream.split(' ')):
            if not word.isdigit():
                sys.stderr.write("Error: Undefined word #{} {}\n".format(i, word))
                sys.stderr.write("Assembly unsucessful!\n")
                sys.exit()
                return None
            
    return result


def int_to_VHDL(i):
    return 'X"{:02}"'.format(i)


def bytecode_to_VHDL(bytecode):
    output = list(map(int_to_VHDL, bytecode))
    return 'signal PROG : ram_type:= ({}, others => X"00");'.format(
            ", ".join(output))



stream = args.input[0].read()
stream = convert_to_bytecode(stream)
stream = bytecode_to_VHDL(stream)


args.output.write(stream)
if args.output == sys.stdout:
    args.output.write('\n')
else:
    args.output.close()