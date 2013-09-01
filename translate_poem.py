'''
Created on Sep 1, 2013

@author: Ethan
'''

import translator
import sys
import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("inputfile", metavar="FILE", help="file to be used as the input poem")
parser.add_argument("-c", "--ccode", metavar="FILE", dest="ccodefile", help="file to store translated C")
parser.add_argument("-o", "--output", metavar="FILE", dest="compiledfile", help="file to store final executable")
args = parser.parse_args()
#parser.add_argument("")
lines = list()

with open(args.inputfile, "r") as f:
    lines = f.readlines()

ccodefile = "output.c"
if args.ccodefile:
    ccodefile = args.ccodefile

try:
    with open(ccodefile, "w") as f:
        for x in translator.translatePoem(lines):
            f.write(x + '\n')
except translator.TranslatorSyntaxError as e:
    print (e)

compiledfile = "output"

if args.compiledfile:
    compiledfile = args.compiledfile

# compile with gcc
os.system("gcc " + ccodefile + " -o " + compiledfile)
# run program
os.system("./" + compiledfile)
