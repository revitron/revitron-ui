import subprocess
import os
import glob
from pyrevit import script
from pyrevit.coreutils import logger
from rpm import config


mlogger = logger.get_logger(__name__)

class Update:
		
	@staticmethod
	def check(repo):  
		mlogger.info('Checking updates for {}'.format(repo))
		try:
			if not os.path.isdir(repo + '\\.git'):
				return False
			if not Update.remoteExists(repo):
				mlogger.error('Remote of repository "{}" not found!'.format(os.path.basename(repo)))
				return False
			status = Update.git('fetch origin --dry-run', repo)
			if status:
				mlogger.info(status)
				return True
		except:
			pass	
   		return False
		
	@staticmethod
	def checkExtensions():
		status = False
		for repo in Update.getExtensionRepos():
			if Update.check(repo):
				status = True
		return status
				
	@staticmethod
	def checkPyRevit():
		return Update.check(config.RPM_PYREVIT_DIR)    
		
	@staticmethod
	def git(cmd, repo):
		return subprocess.check_output('set GIT_TERMINAL_PROMPT=0 && git -c credential.helper= --git-dir={0}\\.git --work-tree={0} {1}'.format(repo, cmd), 
                                 	   stderr=subprocess.STDOUT, 
                                       shell=True, 
                                       cwd='C:\\')
		
	@staticmethod
	def getExtensionRepos():
		repos = []
		for git in glob.glob('{}\\*\\.git'.format(config.RPM_EXTENSIONS_DIR)):
			repos.append(os.path.dirname(git))
		return repos
				
	@staticmethod
	def pyRevit():
		revit = ''
		process = subprocess.Popen(['powershell', 'Get-Process Revit | Select-Object Path'], stdout=subprocess.PIPE)
		while True:
			line = process.stdout.readline()
			if 'Revit' in line:
				revit = line
				break
			if not line:
				break
		os.system('{}\\updatePyRevit.bat "{}" "{}"'.format(os.path.dirname(__file__), config.RPM_PYREVIT_DIR, revit))
	
	@staticmethod 
	def extension(repo, force = False):
		if not Update.remoteExists(repo):
			mlogger.error('Remote of repository "{}" not found!'.format(os.path.basename(repo)))
			return False
		if force:
			print(Update.git('reset --hard HEAD', repo))
			print(Update.git('clean -f -d', repo))
		status = Update.git('status --untracked-files=no --porcelain', repo)
		if status:
			print(status)
			mlogger.warning('Skipped update, repository not clean!')
		else:
			print(Update.git('pull', repo))
	
	@staticmethod
	def extensions(force = False):
		out = script.get_output()
		for repo in Update.getExtensionRepos():
			out.print_html('<br><b>{}</b> &mdash; updating ...'.format(os.path.basename(repo)))
			Update.extension(repo)
   
	@staticmethod
	def remoteExists(repo):
		url = Update.git('remote get-url --all origin', repo).rstrip()
		try:
			Update.git('ls-remote {}'.format(url), repo)
			return True
		except:
			return False