#!/usr/bin/env python3
"""
Module Docstring
"""

import re, sys, os, json, copy, zlib, string, random, math

__author__ = "Igor Terletskiy"
__version__ = "0.0.1"
__license__ = "MIT"


tags = {
	'script': 'script',
	'link': 'style',	
}

def getPathsFrom(content, directory):
	pathsFromTags = []
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	for i in rawTagsList:
		pathsFromTags.append(directory + '/' + re.sub(r'.*?\=', '', re.findall(pathsAttrPattern + r'".*?"', i)[0])[1:-1])
	print(pathsFromTags)
	for i in pathsFromTags:
		t = open(i, 'r+')
		print('********************\n', t.read(), '********************\n')
	return pathsFromTags

def walk(filesList):
	for key in filesList:
		file = open(key, 'r+')
		content = file.read()
		appendPaths = getPathsFrom(content, key[0:key.rfind('/')])


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
	walk(filesList)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()