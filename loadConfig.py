import re, os, shutil, json

def prepareConfig(defaultConfig, config):
	result = {}
	for i in defaultConfig:
		result[i] = config[i] if i in config else defaultConfig[i]
	return result

def loadConfig(filepath = 'linker.config.js'):
	config = json.loads(open(filepath, 'r').read())
	defaultConfig = {
		'entry': './',
		'lazyLoad': False,
		'useMinification': True,
		'rootNode': {
			'tag': 'div',
			'class': '__linker_root_node'
		}
	}
	return prepareConfig(defaultConfig, config)