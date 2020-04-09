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

label_finder = re.compile(r"([a-zA-Z0-9]+):")


def replace_labels(stream):
    """ 
    Find all references to labels and replace them in string.
    
    Arguments:
        stream  --  The assembly stream. Must be cleaned of comments and errors.
                    Assumes that each word is seperated by ' ' and no newlines.
    """
    labels = {}
    i_stream = ""
    for i, word in enumerate(stream.split(' ')):
        if word.endswith(':'):
            labels[word[:-1]] = i - len(labels)
        else:
            i_stream += word + ' '
    for key, value in labels.items():
        i_stream = i_stream.replace(key, str(value))
    return i_stream


def convert_to_bytecode(stream, opcodes):
    """ DOCSTRING:
    Convert all opcodes to their respective bytecodes

    Arguments:
        stream  --  The assembly stream. Must be cleaned of comments and errors.
                    Assumes that each word is seperated by ' ' and no newlines.
                    Assumes that all labels are purged.

        opcodes --  A dictionary of opcodes and their corresponding bytecodes.
                    The program will halt if an opcode not present in this dict
                    appears in the stream.
    """
    for key, value in opcodes.items():
        stream = stream.replace(key, str(value))
    result = []
    for i, word in enumerate(stream.split(' ')):
        if len(word) and not word.isspace():
            result.append(word)
    stream = " ".join(result)
    return stream


def int_to_VHDL(i, size = 2):
    """
    Convert integer into a VHDL-appropriate string

    Arguments:
        i       --  Integer to be converted.
        size    --  Size of the integer in nibbles.
    """
    return ('X"{:0' + str(size) + '}"').format(i)


def bytecode_to_VHDL(bytecode):
    """Convert bytestream into VHDL Code"""
    output = list(map(int_to_VHDL, map(int, bytecode.split(' '))))
    return 'signal PROG : ram_type:= ({}, others => X"00");'.format(
            ", ".join(output))

with args.input[0] as file:
    out = replace_labels(file.read().replace('\n', ' '))
    out = convert_to_bytecode(out, OPCODES)
    out = bytecode_to_VHDL(out)
    args.output.write(out)
    if args.output == sys.stdout:
        args.output.write('\n')
    else:
        args.output.close()
