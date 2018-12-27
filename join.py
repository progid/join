#!/usr/bin/env python3
"""
Module Docstring
"""

import re, sys, os, json, copy, zlib, string, random, math, shutil, htmlmin, cssmin, jsmin
from makeBuild import makeBuild

__author__ = "Igor Terletskiy"
__version__ = "0.0.1"
__license__ = "MIT"

def main():
	directories = sys.argv[1:] if len(sys.argv) > 1 else ['.']
	makeBuild(directories, ['html'])

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()