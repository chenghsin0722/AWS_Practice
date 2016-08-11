#!/usr/bin/env python 

import re
import sys

def log_process(raw_path,process_path):
    inputf = open(raw_path, "r")
    ouputf = open(process_path,"wb")
    for line in inputf.readlines():
        if re.search('NOERROR',line):
            m = re.search('[a-z0-9]{32}\.hashserver.cs.trendmicro.com',line)
            ouputf.write(m.group(0))
            ouputf.write("\n")

    inputf.close()
    ouputf.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Usage: python hash_parser.py [rbldnsd log]'
        sys.exit(-1)

    log_process(sys.argv[1],'/tmp/1.log')
