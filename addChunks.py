import re, os, shutil

def resolveHTMLFilePathFor(tag, path):
	link = path[path.find('"') + 1:path.rfind('"')]
	return tag.replace(link, link[link.rfind('/') + 1:])

def walk(filesList, buildDir):
	for key in filesList:
		file = open(key, 'r+')
		lastSlash = key.rfind('/')
		appendPaths = getPathsFrom(file.read(), key[:lastSlash], key[lastSlash:], buildDir)
		file.close()

def getListOfFiles(directory, ext):
	list = []
	for root, dirs, files in os.walk(directory):  
		for filename in files:
			if re.search(r'.' + ext + '$', filename):
				list.append(root + '/' + filename)
	return list

def addChunks(dirname = 'build'):
	filesList = getListOfFiles(dirname, 'html')
	print(filesList)
