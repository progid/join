import re, os, shutil

def createFolder(dirname, removeIfExists = True):
	if os.path.isdir(dirname) and removeIfExists:
		shutil.rmtree(dirname)
	elif os.path.isdir(dirname) and not removeIfExists:
		return False
	os.mkdir(dirname)

def saveHTMLBuildFile(pathname, content):
	buildFile = open(pathname, 'w+')
	buildFile.write(htmlmin.minify(content))
	buildFile.close()

def resolveHTMLFilePathFor(tag, path):
	link = path[path.find('"') + 1:path.rfind('"')]
	return tag.replace(link, link[link.rfind('/') + 1:])

def walk(filesList, buildDir):
	for key in filesList:
		file = open(key, 'r+')
		lastSlash = key.rfind('/')
		appendPaths = getPathsFrom(file.read(), key[:lastSlash], key[lastSlash:], buildDir)
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

def addChunks(directories, extentions, dirname = 'build'):
	createFolder(dirname)
	createFolder(dirname + '/assets')
	filesList = getListOfFiles(directories, extentions)
	walk(filesList, dirname)