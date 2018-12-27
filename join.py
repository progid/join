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

def makeAnchorLink(filepath):
	return '<a href="' + filepath[filepath.rfind('/') + 1:] + '">'

def makeLinkFor(tag, filepath):
	content = open(filepath, 'r+').read()
	if tag == 'script':
		return makeScript(content)
	elif tag == 'link':
		return makeStyle(content)
	elif tag == 'a':
		return makeAnchorLink(filepath)
	else:
		return False

def getPathsFrom(content, directory, filename, buildDir):
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	print(filename)
	for i in rawTagsList:
		tag = re.findall(r'<\w+', i)[0][1:]
		link = re.findall(pathsAttrPattern + r'".*?"', i)[0]
		path = directory + '/' + re.sub(r'.*?\=', '', link)[1:-1]
		linkContent = makeLinkFor(tag, path)
		content = content.replace(i, linkContent if linkContent else i)
	buildFile = open(buildDir + filename, 'w+')
	buildFile.write(content)
	buildFile.close()
	return True

def walk(filesList, buildDir = 'build'):
	for key in filesList:
		file = open(key, 'r+')
		appendPaths = getPathsFrom(file.read(), key[0:key.rfind('/')], key[key.rfind('/'):], buildDir)
		file.close()

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
	if os.path.isdir(dirname):
		shutil.rmtree(dirname)
	os.mkdir(dirname)

def main():
	directories = sys.argv[1:] if len(sys.argv) > 1 else ['.']
	makeBuild()
	extentions = ['html']
	filesList = getListOfFiles(directories, extentions)
	walk(filesList)

if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()