#!/usr/bin/env python3
"""
Module Docstring
"""

import re, sys, os, json, copy, zlib, string, random, math

__author__ = "Igor Terletskiy"
__version__ = "0.0.1"
__license__ = "MIT"

def makeStyle(styles):
	return '<style>' + styles + '</style>'

def makeScript(script):
	return '<script>' + script

def makeLinkFor(tag, content):
	if tag == 'script':
		return makeScript(content)
	elif tag == 'link':
		return makeStyle(content)
	else:
		return ''

def getPathsFrom(file, directory):
	content = file.read()
	pathsFromTags = []
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	for i in rawTagsList:
		tag = re.findall(r'<\w+', i)[0][1:]
		link = re.findall(pathsAttrPattern + r'".*?"', i)[0]
		path = directory + '/' + re.sub(r'.*?\=', '', link)[1:-1]
		tempFile = open(path, 'r+')
		content = content.replace(i, makeLinkFor(tag, tempFile.read()))
	file.seek(0)
	file.write(content)
	file.truncate()
	file.close()
		
	return pathsFromTags

def walk(filesList):
	for key in filesList:
		file = open(key, 'r+')
		appendPaths = getPathsFrom(file, key[0:key.rfind('/')])

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