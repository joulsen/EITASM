# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:38:54 2020

@author: Andreas
"""

import re
import os
import json

RE_INCLUDE = r"#include [\"\'](.+)[\"\']"
RE_INCLUDE_LIB = r"#include (\w+)"
RE_HEX = r"(0x([\dABCDEF]+))"
RE_BIN = r"(0b([01]+))"
RE_EMPTY_LINES = r"(^((\/\/|;).*|\s*)\n)"
RE_COMMENT = r"(\s*(\/\/|;).*)"
RE_IMMEDIATE = r"(\w+)(.+\$)"

DEBUG_FLAG = 1

def add_includes(program, path=__file__):
    N_INC = 0
    for match in re.finditer(RE_INCLUDE_LIB, program, re.I):
        input_file = open(os.path.join(os.path.dirname(__file__), "../", "include", match.group(1) + ".asm"))
        program = program.replace(match.group(0), input_file.read())
        N_INC += 1
    for match in re.finditer(RE_INCLUDE, program, re.I):
        input_file = open(os.path.join(os.path.dirname(path), match.group(1)), 'r')
        program = program.replace(match.group(0), input_file.read())
        N_INC += 1
    if DEBUG_FLAG: print("{} files included.".format(N_INC))
    return program

def unify_words(program):
    try:
        numbers, values = list(map(list, zip(*re.findall(RE_HEX, program))))
        values = list(map(lambda i: str(int(i, 16)), values))
        for pair in sorted(zip(numbers, values), key=lambda s: -len(s[0])):
            program = re.sub(*pair, program)
        numbers, values = list(map(list, zip(*re.findall(RE_BIN, program))))
        values = list(map(lambda i: str(int(i, 2)), values))
        for pair in sorted(zip(numbers, values), key=lambda s: -len(s[0])):
            program = re.sub(*pair, program)
    except ValueError:
        pass
    if DEBUG_FLAG: print("Hexadecimal and binary numbers parsed.")
    return program

def clean(program):
    N_ORIG = len(program)
    program = re.sub(RE_EMPTY_LINES, "", program, flags=re.M)
    program = re.sub(RE_COMMENT, "", program)
    if DEBUG_FLAG: print("{} characters of comments and whitespace removed.".format(N_ORIG - len(program)))
    return program.strip()

def replace_labels(program):
    new_program = ""
    pc = 0
    labels = {}
    for i, line in enumerate(program.split('\n')):
        if ':' in line:
            label = line[:line.find(':')]
            if re.search(r"^[A-Za-z0-9_]+$", label) is None:
                raise ValueError('Illegal character(s) in label "{}"'.format(label))
            else:
                labels[label] = pc
        else:
            new_program += line + '\n'
            pc += 1
    for label, value in sorted(labels.items(), key=lambda s: -len(s[0])):
        new_program = re.sub("GOTO {}".format(label),
                             "GOTO {}".format(str(value)), new_program)
    if DEBUG_FLAG: print("{} labels replaced.".format(len(labels)))
    return new_program.strip()


def expound_immediate(program):
    N_ORIG = len(program)
    program = re.sub(RE_IMMEDIATE, r"\1i\2", program)
    if DEBUG_FLAG: print("{} immediate commands added.".format(len(program) - N_ORIG))
    return program

def lazy_int(s):
    try:
        return int(s)
    except ValueError:
        return s

replacement = {'rv': "{:01X}{:04X}",
               'r' : "{:01X}{}0000",
               'v' : "0{:04X}{}",
               ''  : "00000{}{}"}
def insert_bytecodes(program, opcodes):
    new_program = ""
    for op, arg1, arg2 in re.findall(r"^(\w+) ?(\d+)? ?\$?(\d+)?", program, flags=re.M):
        new_program += opcodes[op]["bytecode"] + replacement[opcodes[op]["type"]].format(lazy_int(arg1), lazy_int(arg2))
        new_program += '\n'
    if DEBUG_FLAG: print("{} bytecodes inserted.".format(len(new_program.split('\n')) - 1))
    return new_program

def bytecode_to_vhdl(program):
    prefix = "signal PROG : ram_type := ("
    suffix = 'others => x"0000000");'
    content = ""
    for line in program.split('\n'):
        if line != '':
            content += 'x"{:07x}", '.format(int(line, 16))
    return prefix + content + suffix

def bytecode_to_ram_init(program, filepath, comment):
    comment = "; Compiled from {}\n; {}\n".format(filepath, comment)
    prefix = "memory_initialization_radix=16;\nmemory_initialization_vector=\n"
    content = ""
    for i, line in enumerate(program.split('\n')):
        if line != '':
            content += "{:07x},\n".format(int(line, 16))
    content = content[:-2] + ";"
    if DEBUG_FLAG: print("Bytecode assembled to RAM content.")
    return comment + prefix + content

def assemble(program, opcodes):
    return insert_bytecodes(replace_labels(expound_immediate(unify_words(clean(program)))), opcodes)

def assemble_to_ram(iFile, opcodes, oFile=None, comment=''):
    opcodes = json.load(opcodes)
    program = iFile.read()
    program = clean(program)
    program = add_includes(program, iFile.name)
    program = expound_immediate(unify_words(program))
    program = insert_bytecodes(replace_labels(program), opcodes)
    program = bytecode_to_ram_init(program, iFile.name, comment)
    if oFile is None:
        oFile = open(os.path.splitext(iFile.name)[0] + ".coe", 'w')
    oFile.write(program)
    oFile.close()
    iFile.close()
    if DEBUG_FLAG: print("Program sucessfully compiled to {}".format(oFile.name))
    return program
