#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:32:34 2020

@author: Andreas
"""

import re
import json

def get_opcodes(filepath):
    opcodes = {}
    with open(filepath, 'r') as file:
        for bytecode, mneumonic in re.findall(r'X"(\d+)" => -- \[(\w+)\]',
                                              file.read()):
            opcodes[mneumonic] = int(bytecode)
    return opcodes

def dump_opcodes(opcodes, filepath):
    with open(filepath, 'w') as file:
        json.dump(opcodes, file)