#!/usr/bin/python2

'''
This is the assembler I wrote for the bored assembly
'''

import sys
import struct

if len(sys.argv) < 3:
    print "usage {0} inFile.bd out".format(sys.argv[0])
    exit(-1)

csm_file = open(sys.argv[1])
code_file = open(sys.argv[2], "wb")

def pack(a):
    return struct.pack("I", a)

def get_reg(op):
    return ["r0","r1","r2","r3"].index(op)

def both_reg(op1, op2):
    return op1 in ["r0","r1","r2","r3"] and op2 in ["r0","r1","r2","r3"]

def is_reg(op):
    return op in ["r0","r1","r2","r3"]

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
    if cur[0] == ";":
        pass
    elif cur[0] == "exit":
        write([0x00])
    elif cur[0] == "nop":
        write([0x90])
    elif cur[0] == "display":
        write([0x91])

    #mov
    elif cur[0] == "mov":
        if both_reg(cur[1], cur[2]):
            write([0x1, get_reg(cur[1]), get_reg(cur[2])])
            #code_file.write(pack(0x1)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(int(cur[2]))+pack(0x0))
        elif is_reg(cur[1]) and not is_reg(cur[2]):
            write([0x2, get_reg(cur[1]), int(cur[2])])
            #code_file.write(pack(0x2)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))

    #cmp
    elif cur[0] == "cmp":
        if cur[1] in ["r0","r1","r2","r3"] and cur[2] in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x10)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))

    #math
    #elif cur[0] == "add":
    #    if cur[1]

    #jmp
    elif cur[0] == "jmp":
        code_file.write(pack(0x30)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))
    elif cur[0] == "je":
        code_file.write(pack(0x31)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))

    #stop on unknown instruction
    else:
        print "Instruction not understood"
        csm_file.close()
        code_file.close()
        exit(-2)

csm_file.close()
code_file.close()
