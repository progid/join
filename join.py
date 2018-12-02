#!/usr/bin/env python3
"""
Module Docstring
"""

import re, sys, os, json, copy, zlib, string, random, math

__author__ = "Igor Terletskiy"
__version__ = "0.0.1"
__license__ = "MIT"

def parseHTMLAttrs(tag):
	

def parseHTMLTags(file):


def analyseDependencies(filesList):
	for key in filesList:
		file = open(key, 'r+')
		content = file.read()
		

def getListOfFiles(dir, extentions):
	list = []
	for directory in dir:
		for root, dirs, files in os.walk(directory):  
			for filename in files:
				for ext in extentions:
					if re.search(r'.' + ext + '$', filename):
						list.append(root + '/' + filename)
	return list

def main():
	directories = sys.argv[1:] if len(sys.argv) > 1 else ['.']
	extentions = ['html']
	filesList = getListOfFiles(directories, extentions)
	analyseDependencies(filesList)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()