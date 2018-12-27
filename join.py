#!/usr/bin/env python3
"""
Module Docstring
"""

import re, sys, os, json, copy, zlib, string, random, math, shutil

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

def getPathsFrom(file, filename, buildDir):
	content = file.read()
	buildFile = open(buildDir + filename, 'w+')
	pathsFromTags = []
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	print(filename)
	for i in rawTagsList:
		tag = re.findall(r'<\w+', i)[0][1:]
		link = re.findall(pathsAttrPattern + r'".*?"', i)[0]
		path = directory + '/' + re.sub(r'.*?\=', '', link)[1:-1]
		tempFile = open(path, 'r+')
		content = content.replace(i, makeLinkFor(tag, tempFile.read()))
	buildFile.seek(0)
	buildFile.write(content)
	buildFile.truncate()
	buildFile.close()
	file.close()
		
	return pathsFromTags

def walk(filesList, buildDir = 'build'):
	for key in filesList:
		file = open(key, 'r+')
		appendPaths = getPathsFrom(file, key[key.rfind('/'):], buildDir)

def getListOfFiles(dir, extentions):
	list = []
	for directory in dir:
		for root, dirs, files in os.walk(directory):  
			for filename in files:
				for ext in extentions:
					if re.search(r'.' + ext + '$', filename):
						list.append(root + '/' + filename)
	return list

def makeBuild(dirname = 'build'):
	if not os.path.isdir(dirname):
		os.mkdir(dirname)
		print('Directory "' + dirname + '" was successfully created.')
	else:
		print('Directory "' + dirname + '" already exists.')
		print('Removing...')
		shutil.rmtree(dirname)
		print('Removed')
		print('Creating new directory....')
		os.mkdir(dirname)
		print('Created new "' + dirname + '" directory.')

def main():
	directories = sys.argv[1:] if len(sys.argv) > 1 else ['.']
	makeBuild()
	extentions = ['html']
	filesList = getListOfFiles(directories, extentions)
	walk(filesList)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()