import re, os, shutil, htmlmin, cssmin, jsmin

assetTypes = {
	'imgs': {'jpg', 'jpeg', 'png', 'svg', 'raw', 'gif'},
	'fonts': {'ttf'},
	'data': {'json', 'csv'},
	'sounds': {'mp3', 'wav', 'aac', 'flac'}
}

linkers = {
	'script': lambda c, b: '<script>' + jsmin.jsmin(c),
	'link': lambda c, b: '<style>' + resolveCSSDependencies(cssmin.cssmin(c), b) + '</style>'
}

def createFolder(dirname, removeIfExists = True):
	if os.path.isdir(dirname):
		shutil.rmtree(dirname)
	os.mkdir(dirname)

def makeLinkFor(tag, filepath, buildDir):
	content = open(filepath, 'r+').read()
	return linkers[tag](content, buildDir) if tag in linkers else False

def saveHTMLBuildFile(pathname, content):
	buildFile = open(pathname, 'w+')
	buildFile.write(htmlmin.minify(content))
	buildFile.close()

def resolveHTMLFilePathFor(tag, path):
	link = path[path.find('"') + 1:path.rfind('"')]
	return tag.replace(link, link[link.rfind('/') + 1:])

def resolveCSSDependencies(content, dirname):
	assetsPath = dirname + '/assets'
	createFolder(assetsPath)
	paths = re.findall('url' + r'[\r\n\b\t\s]*' + r'\(' + r'.*?' + r'\)', content)
	for i in paths:
		rawFilePath = i[i.find('url(')+4:i.rfind(')')]
		preparedFilePath = rawFilePath[1:-1] if rawFilePath[0] in ['\'', '"', '`'] else rawFilePath
		filetype = preparedFilePath[preparedFilePath.rfind('.'):]
		print(filetype)
	print('\n*******************************\n')
	return content

def getPathsFrom(content, directory, filename, buildDir):
	pathsAttrPattern = r'(?:(?:href=)|(?:src=))'
	findTagsPattern = r'<.*?' + pathsAttrPattern + r'.*?>'
	rawTagsList = re.findall(findTagsPattern, content)
	for i in rawTagsList:
		tag = re.findall(r'<\w+', i)[0][1:]
		link = re.findall(pathsAttrPattern + r'".*?"', i)[0]
		path = directory + '/' + re.sub(r'.*?\=', '', link)[1:-1]
		linkContent = makeLinkFor(tag, path, buildDir)
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
	createFolder(dirname)
	filesList = getListOfFiles(directories, extentions)
	walk(filesList, dirname)