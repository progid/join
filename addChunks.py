import re, os, shutil, collections, json

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

def prepareFiles(filelist):
	return dict(collections.ChainMap(*[prepareFile(open(item, 'r+'), item[:item.find('/') + 1]) for item in filelist]))

def prepareAnchorsToDOM(rawAnchors):
	splittedAnchors = [[*item.replace('href', 'data-routepath').split(), 'onclick=setRoute(event)'] for item in rawAnchors]
	return [' '.join(item) for item in splittedAnchors]

def prepareDictToDOM(routesDict):
	for key in routesDict:
		anchorTags = findAnchorTagsInFile(routesDict[key]['body'])
		preparedAnchorTags = prepareAnchorsToDOM(anchorTags)
		for index in range(len(anchorTags)):
			routesDict[key]['body'] = routesDict[key]['body'].replace(anchorTags[index],preparedAnchorTags[index])
	return routesDict

def prepareFile(file, rootPath):
	content = file.read()
	anchorTags = findAnchorTagsInFile(content)
	routerLinks = getRouterLinks(anchorTags)
	routesDict = generateRoutesDictFrom(routerLinks, rootPath)
	return routesDict

def getRouterLinks(rawAnchors):
	return [''.join(filter(lambda x: 'href' in x, item.split()))[5:] for item in rawAnchors]

def generateRoutesDictFrom(linksList, rootPath):
	return {
		item: {
			'head': getDepHead(open(rootPath + item, 'r').read()),
			'body': getDepBody(open(rootPath + item, 'r').read())
		} for item in linksList
	}


def getDepHead(depContent):
	content = depContent
	rawHead = content[content.find('<head'):content.rfind('</head>')]
	preparedHead = rawHead[rawHead.find('>') + 1:]
	return preparedHead

def getDepBody(depContent):
	content = depContent
	rawBody = content[content.find('<body'):content.rfind('</body>')]
	preparedBody = rawBody[rawBody.find('>') + 1:]
	return preparedBody

def getEntryFile(entry, rootPath):
	return generateRoutesDictFrom([entry], rootPath + '/')

def buildOutputFile(entry, rootPath, routes, filename = 'index.html'):
	entryfile = prepareDictToDOM(getEntryFile(entry, rootPath))
	y = '<script>function setRoute(e) {document.head.innerHTML = window.__ROUTES[e.currentTarget.getAttribute(\'data-routepath\')].head; document.body.innerHTML = window.__ROUTES[e.currentTarget.getAttribute(\'data-routepath\')].body;}; window.__ROUTES = (' + json.dumps(routes, sort_keys=True, indent=4, ensure_ascii=False).replace('</script>', r'<\/script>') + ') </script>'
	html = '<!DOCTYPE html><html><head>' + entryfile[entry]['head'] + '</head><body>' + entryfile[entry]['body'] + y + '</body></html>'
	output = open(rootPath + '/' + filename, 'w+')
	output.write(html)
	output.close()
	print('DONE...\n')
	return True

def findAnchorTagsInFile(content): 
	rawTagList = re.findall(r'<[^>]*', content)
	anchorTagsInPage = filter(lambda x: r'<a' in x and "href" in x, rawTagList)
	return list(anchorTagsInPage)

def addChunks(dirname = 'build'):
	filesList = getListOfFiles(dirname, 'html')
	prepared = prepareFiles(filesList)
	prepareDictToDOM(prepared)
	buildOutputFile('main.html', dirname, prepared)
