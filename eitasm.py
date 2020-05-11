#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:18:37 2020

@author: Andreas
"""

import argparse
import os
from lib.assembler import assemble_to_ram

def __is_valid_file_open(path):
    if os.path.isfile(path):
        return open(path, 'r')
    else:
        argparse.ArgumentTypeError("{} is not a valid input path!".format(path))


parser = argparse.ArgumentParser(description="Assembler for Supercigar's CPU")
parser.add_argument('input', metavar='I',
                    help="Input file for assembly code",
                    type=__is_valid_file_open, nargs=1)

parser.add_argument('-o', metavar='--output', dest="output", type=str,
                    help="Output file for RAM initialization code",
                    nargs='?')

parser.add_argument('-op', metavar='--opcodes', dest="opcodes",
                    help="Specifies location of opcode JSON (default opcodes.json)",
                    type=argparse.FileType('r'), nargs='?',
                    default=os.path.join(os.path.dirname(__file__), "opcodes.json"))

parser.add_argument('-c', metavar='--comment', dest="comment",
                    help="Comment that will be placed into header of RAM file.",
                    type=str, nargs='?', default="")

args = parser.parse_args()


if __name__ == "__main__":
    if args.output != None:
        args.output = open(args.output, 'w')
    assemble_to_ram(args.input[0], args.opcodes, args.output, args.comment)
