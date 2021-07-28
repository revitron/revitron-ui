from rpm import config
from pyrevit import script
from pyrevit.coreutils import logger
from datetime import datetime
import os
import json
import subprocess

mlogger = logger.get_logger(__name__)


class ExtensionsManager:

	def __init__(self):
		self.json = config.RPM_EXTENSIONS_DIR + '\\rpm.json'

	def getInstalled(self):
		try:
			with open(self.json) as jsonFile:
				data = json.load(jsonFile)
		except:
			data = {'installed': dict()}
		return data['installed']

	def removeAll(self):
		for key, ext in self.getInstalled().iteritems():
			try:
				subprocess.check_output(
				    'rmdir /Q /S {}'.format(ext['path']),
				    stderr=subprocess.STDOUT,
				    shell=True,
				    cwd='C:\\'
				)
				mlogger.info('Removed extension {}'.format(key))
			except:
				mlogger.error('Error removing extension {}'.format(key))
		data = {'installed': dict()}
		script.dump_json(data, self.json)

	def install(self, name, repo, extType):
		repo = repo.replace('.git', '') + '.git'
		cmd = '{} extend {} {} {} --dest="{}"'.format(
		    config.RPM_PYREVIT_BIN, extType, name, repo, config.RPM_EXTENSIONS_DIR
		)
		types = {'ui': 'extension', 'lib': 'lib'}
		path = config.RPM_EXTENSIONS_DIR + '\\' + name + '.' + types.get(
		    extType, 'extension'
		)
		try:
			if not os.path.isdir(path):
				subprocess.check_output(
				    cmd, stderr=subprocess.STDOUT, shell=True, cwd='C:\\'
				)
				mlogger.info('Installed extension {}'.format(name))
			else:
				mlogger.error('{} is not empty!'.format(path))
			self.register(name, repo, extType, path)
		except:
			mlogger.error('Installing {} has failed!'.format(name))

	def register(self, name, repo, extType, path):
		data = {'installed': self.getInstalled()}
		data['installed'][os.path.basename(path)] = {
		    'name': name,
		    'type': extType,
		    'repo': repo,
		    'path': path,
		    'date': str(datetime.now())
		}
		script.dump_json(data, self.json)
