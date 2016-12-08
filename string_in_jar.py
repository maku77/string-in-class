#!/usr/bin/env python
"""
Extracts all string literals in Java classes in JAR.
This needs Python (>= 3.5) and JDK (for javap) to be installed.

Usage: python string_in_jar.py <jar_file>
"""

import zipfile
import os
import re
import subprocess
import sys

def command(cmd):
    """ Runs a command and iterates its output. """
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print('Could not execute command [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def iter_classes_in_jar(jar_name):
    """ Iterates all classes in the specified JAR file. """
    with zipfile.ZipFile(jar_name, 'r') as zf:
        arr = list(zf.infolist())
        arr.sort(key=lambda x: x.filename)
        for info in arr:
            classname, ext = os.path.splitext(info.filename)
            if ext != '.class':
                continue
            yield classname

def print_literal(line):
    """ Prints a string literal if the line includes. """
    match = re.search(r'// String (.+)', line)
    if match:
        print(match.group(1))

if __name__ == '__main__':
    inputfile = sys.argv[1]
    for clazz in iter_classes_in_jar(inputfile):
        cmd = 'javap -cp {} -c {}'.format(inputfile, clazz)
        for line in command(cmd):
            print_literal(line)

