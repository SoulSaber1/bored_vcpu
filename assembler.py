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

for l in csm_file.readlines():
    cur = l.strip().split(" ")
    if "-v" in sys.argv:
        print cur

    #utility
    if cur[0] == ";":
        pass
    elif cur[0] == "display":
        code_file.write(pack(0x91)+pack(0x0)+pack(0x0)+pack(0x0))
    elif cur[0] == "exit":
        code_file.write(pack(0x0)+pack(0x0)+pack(0x0)+pack(0x0))
    elif cur[0] == "nop":
        code_file.write(pack(0x90)+pack(0x0)+pack(0x0)+pack(0x0))

    #mov
    elif cur[0] == "mov":
        if cur[1] in ["r0","r1","r2","r3"] and cur[2] not in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x1)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(int(cur[2]))+pack(0x0))
        elif cur[1] in ["r0","r1","r2","r3"] and cur[2] in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x2)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))

    #cmp
    elif cur[0] == "cmp":
        if cur[1] in ["r0","r1","r2","r3"] and cur[2] in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x10)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))

    #jmp
    elif cur[0] == "jmp":
        code_file.write(pack(0x30)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))
    elif cur[0] == "je":
        code_file.write(pack(0x31)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))

    else:
        print "Instruction not understood"
        exit(-2)

csm_file.close()
code_file.close()
