#!/usr/bin/env python
"""
Extracts all string literals in Java classes.
This needs Python (>= 3.5) and JDK (for javap) to be installed.

Usage: python string_in_class.py <jar_file | class_file>
"""

import zipfile
import os
import re
import subprocess
import sys


class LiteralExtractor:
    def __init__(self):
        self.PAT = re.compile(r'= String\s+#\d+\s+// (.+)')

    def extract(self, line):
        """
        Extract a string literal in the specified line.
        Returns None if not found.
        """
        match = self.PAT.search(line)
        if match:
            return match.group(1)
        return None

    def extract_and_print(self, line):
        literal = self.extract(line)
        if literal:
            print(literal)


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


if __name__ == '__main__':
    inputfile = sys.argv[1]
    extractor = LiteralExtractor()

    if inputfile.endswith('.class'):
        cmd = 'javap -v {}'.format(inputfile)
        for line in command(cmd):
            extractor.extract_and_print(line)
    else:  # Probably it is a JAR
        for clazz in iter_classes_in_jar(inputfile):
            cmd = 'javap -cp {} -v {}'.format(inputfile, clazz)
            for line in command(cmd):
                extractor.extract_and_print(line)

