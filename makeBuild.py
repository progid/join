import re, os, shutil, htmlmin, cssmin, jsmin

linkers = {
	'script': lambda c: '<script>' + jsmin.jsmin(c),
	'link': lambda c: '<style>' + cssmin.cssmin(c) + '</style>'
}

def makeLinkFor(tag, filepath):
	content = open(filepath, 'r+').read()
	return linkers[tag](content) if tag in linkers else False

def saveHTMLBuildFile(pathname, content):
	buildFile = open(pathname, 'w+')
	buildFile.write(htmlmin.minify(content))
	buildFile.close()

def resolveHTMLFilePathFor(tag, path):
	link = path[path.find('"') + 1:path.rfind('"')]
	return tag.replace(link, link[link.rfind('/') + 1:])

def getPathsFrom(content, directory, filename, buildDir):
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	for i in rawTagsList:
		tag = re.findall(r'<\w+', i)[0][1:]
		link = re.findall(pathsAttrPattern + r'".*?"', i)[0]
		path = directory + '/' + re.sub(r'.*?\=', '', link)[1:-1]
		linkContent = makeLinkFor(tag, path)
		linkContent = linkContent if linkContent else resolveHTMLFilePathFor(i, link)
		content = content.replace(i, linkContent)
		saveHTMLBuildFile(buildDir + filename, content)
	return True

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

def makeBuild(directories, extentions, dirname = 'build'):
	if os.path.isdir(dirname):
		shutil.rmtree(dirname)
	os.mkdir(dirname)
	filesList = getListOfFiles(directories, extentions)
	walk(filesList, dirname)