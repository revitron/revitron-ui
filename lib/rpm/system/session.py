from pyrevit import script
from pyrevit.loader import sessionmgr
from pyrevit.loader import sessioninfo


class Session:

	@staticmethod
	def reload():
		logger = script.get_logger()
		results = script.get_results()
		logger.info('Reloading ...')
		sessionmgr.reload_pyrevit()
		results.newsession = sessioninfo.get_session_uuid()