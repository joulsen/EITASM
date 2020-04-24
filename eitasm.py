#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:18:37 2020

@author: Andreas
"""

import argparse
import json
import os
from lib.assembler import assemble

def __is_valid_file_open(path):
    if os.path.isfile(path):
        return open(path, 'r')
    else:
        argparse.ArgumentTypeError("{} is not a valid input path!".format(path))


parser = argparse.ArgumentParser(description="Assembler for Supercigar's CPU")
parser.add_argument('input', metavar='I',
                    help="Input file for assembly code",
                    type=__is_valid_file_open, nargs=1)

parser.add_argument('output', metavar='O', type=str,
                    help="Output file for VHDL code",
                    nargs='?')

parser.add_argument('opcodes', metavar='--opcodes',
                    help="Specifies location of opcode JSON (default opcodes.json)",
                    type=argparse.FileType('r'), nargs='?', default="opcodes.json")

args = parser.parse_args()
opcodes = json.load(args.opcodes)

if __name__ == "__main__":
    if args.output is None:
        output_file = open(os.path.splitext(args.input[0].name)[0] + ".vhd", 'w')
    else:
        output_file = open(args.output, 'w')
    output_file.write(assemble(args.input[0].read(), opcodes))
    output_file.close()
    print("Program compiled successfully to file '{}'".format(output_file.name))