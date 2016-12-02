#!/usr/bin/python2

'''
This is the assembler I wrote for the bored assembly
'''

import sys
import struct

if len(sys.argv) < 3:
    print "usage {0} inFile.bd out [-v]".format(sys.argv[0])
    exit(-1)

csm_file = open(sys.argv[1])
code_file = open(sys.argv[2], "wb")

def pack(a):
    return struct.pack("I", a)

def both_reg(op1, op2):
    return op1 in ["r0","r1","r2","r3"] and op2 in ["r0","r1","r2","r3"]

def is_reg(op):
    return op in ["r0","r1","r2","r3"]

def get_reg(op):
    return ["r0","r1","r2","r3"].index(op)

def is_mem(op):
    return op[0] == "[" and op[-1] == "]"

def get_mem(op):
    return get_val(op[1:-1])

def is_val(op):
    return not is_mem(op) and not is_reg(op)

def get_val(op):
    return int(op)

def write(vals):
    global code_file
    written = 0
    for v in vals:
        code_file.write(pack(v))
        written += 1
    while written < 4:
        code_file.write(pack(0x0))
        written += 1

for l in csm_file.readlines():
    cur = l.strip().split(" ")

    if "-v" in sys.argv:
        print cur

    #utility
    if cur[0][0] == ";":
        pass
    elif cur[0] == "exit":
        write([0x00])
    elif cur[0] == "nop":
        write([0x90])
    elif cur[0] == "cpu":
        write([0x91])
    elif cur[0] == "mem":
        write([0x92])

    #mov
    elif cur[0] == "mov":
        if both_reg(cur[1], cur[2]):
            write([0x1, get_reg(cur[1]), get_reg(cur[2])])
        elif is_reg(cur[1]) and is_val(cur[2]):
            write([0x2, get_reg(cur[1]), get_val(cur[2])])
        elif is_mem(cur[1]) and is_reg(cur[2]):
            write([0x3, get_mem(cur[1]), get_reg(cur[2])])
        elif is_mem(cur[1]) and is_val(cur[2]):
            write([0x4, get_mem(cur[1]), get_val(cur[2])])
        elif is_reg(cur[1]) and is_mem(cur[2]):
            write([0x5, get_reg(cur[1]), get_mem(cur[2])])

    #cmp
    elif cur[0] == "cmp":
        if both_reg(cur[1], cur[2]):
            write([0x10, get_reg(cur[1]), get_reg(cur[2])])
    #math
    elif cur[0] == "add":
        if both_reg(cur[1], cur[2]):
            write([0x20, get_reg(cur[1]), get_reg(cur[2])])
        elif is_reg(cur[1]) and is_val(cur[2]):
            write([0x21, get_reg(cur[1]), get_val(cur[2])])
        elif is_reg(cur[1]) and is_mem(cur[2]):
            write([0x22, get_reg(cur[1]), get_mem(cur[2])])
        elif is_mem(cur[1]) and is_reg(cur[2]):
            write([0x23, get_mem(cur[1]), get_reg(cur[2])])
        elif is_mem(cur[1]) and is_val(cur[2]):
            write([0x24, get_mem(cur[1]), get_val(cur[2])])
        elif is_mem(cur[1]) and is_mem(cur[2]):
            write([0x2a, get_mem(cur[1]), get_mem(cur[2])])
    elif cur[0] == "sub":
        if both_reg(cur[1], cur[2]):
            write([0x25, get_reg(cur[1]), get_reg(cur[2])])
        elif is_reg(cur[1]) and is_val(cur[2]):
            write([0x26, get_reg(cur[1]), get_val(cur[2])])
        elif is_reg(cur[1]) and is_mem(cur[2]):
            write([0x27, get_reg(cur[1]), get_mem(cur[2])])
        elif is_mem(cur[1]) and is_reg(cur[2]):
            write([0x28, get_mem(cur[1]), get_reg(cur[2])])
        elif is_mem(cur[1]) and is_val(cur[2]):
            write([0x29, get_mem(cur[1]), get_val(cur[2])])
        elif is_mem(cur[1]) and is_mem(cur[2]):
            write([0x2b, get_mem(cur[1]), get_mem(cur[2])])

    #jmp
    elif cur[0] == "jmp":
        write([0x40, 8*get_val(cur[1])])
    elif cur[0] == "je":
        write([0x41, 8*get_val(cur[1])])

    #interrupt
    elif cur[0] == "int":
        write([0x100, get_val(cur[1])])    

    #stop on unknown instruction
    else:
        print "Instruction not understood"
        print cur
        csm_file.close()
        code_file.close()
        exit(-2)

csm_file.close()
code_file.close()
