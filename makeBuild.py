import re, os, shutil, htmlmin, cssmin, jsmin

linkers = {
	'script': lambda c: '<script>' + jsmin.jsmin(c),
	'link': lambda c: '<style>' + cssmin.cssmin(c) + '</style>'
}

def makeLinkFor(tag, filepath):
	content = open(filepath, 'r+').read()
	return linkers[tag](content) if tag in linkers else False

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
	buildFile.write(htmlmin.minify(content))
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

def makeBuild(directories, extentions, dirname = 'build'):
	if os.path.isdir(dirname):
		shutil.rmtree(dirname)
	os.mkdir(dirname)
	filesList = getListOfFiles(directories, extentions)
	walk(filesList)