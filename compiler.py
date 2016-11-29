#!/usr/bin/python2

import sys
import struct

csm_file = open("code.csm")
code_file = open("code", "wb")

def pack(a):
    return struct.pack("I", a)

for l in csm_file.readlines():
    cur = l.strip().split(" ")
    print cur
    if cur[0] == ";":
      pass
    elif cur[0] == "exit":
        code_file.write(pack(0x0)+pack(0x0)+pack(0x0)+pack(0x0))
    elif cur[0] == "nop":
        code_file.write(pack(0x90)+pack(0x0)+pack(0x0)+pack(0x0))
    elif cur[0] == "mov":
        if cur[1] in ["r0","r1","r2","r3"] and cur[2] not in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x1)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(int(cur[2]))+pack(0x0))
        elif cur[1] in ["r0","r1","r2","r3"] and cur[2] in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x2)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))
    elif cur[0] == "cmp":
        if cur[1] in ["r0","r1","r2","r3"] and cur[2] in ["r0","r1","r2","r3"]:
            code_file.write(pack(0x10)+pack(["r0","r1","r2","r3"].index(cur[1]))+pack(["r0","r1","r2","r3"].index(cur[2]))+pack(0x0))
    elif cur[0] == "display":
        code_file.write(pack(0x91)+pack(0x0)+pack(0x0)+pack(0x0))
    elif cur[0] == "jmp":
        code_file.write(pack(0x30)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))
    elif cur[0] == "je":
        code_file.write(pack(0x31)+pack(8*int(cur[1]))+pack(0x0)+pack(0x0))
    else:
        pass

csm_file.close()
code_file.close()
