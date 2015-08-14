#!/usr/bin/env python

from subprocess import call,PIPE, Popen
from os.path import expanduser
from sys import version_info
from argparse import ArgumentParser
import toml

def test_port(ip,port,udp=False):
    port = str(port)
    if udp:
        cmd = ("/usr/bin/nc","-z","-w2","-u",ip,port)
    else:
        cmd = ("/usr/bin/nc","-z","-w2",ip,port)
    ret = call(cmd)
    if ret:
        if udp:
            print("%s:%s/udp is not open"%(ip,port))
        else:
            print("%s:%s/tcp is not open"%(ip,port))

def test_machine(ip,tcp_ports=None,udp_ports=None,extra_tests=None):
    ret = call(("ping","-c1","-W1",ip),stdout=PIPE)
    if ret:
        print("Couldn't ping '%s'"%ip)
    else:
        if tcp_ports:
            for port in tcp_ports:
                test_port(ip,port)
        if udp_ports:
            for port in udp_ports:
                test_port(ip,port,udp=True)
        if extra_tests:
            for t in extra_tests:
                t()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("cfg_file")
    args = parser.parse_args()

    config = toml.load(args.cfg_file)
    for addr,opts in config.items():
        if "extra_tests" in opts:
            opts["extra_tests"] = [ lambda: call(x["script"]) for x in opts["extra_tests"].values() ]
        test_machine(addr,**opts)
