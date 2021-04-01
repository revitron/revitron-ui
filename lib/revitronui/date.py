from datetime import datetime


class Date:


	@staticmethod
	def diff(dateA, dateB):
		dateFormat = '%Y-%m-%d %H:%M:%S'
		started = datetime.strptime(dateA, dateFormat)
		finished = datetime.strptime(dateB, dateFormat)
		dateDiff = finished - started
		minutes = round(dateDiff.total_seconds() / 60, 2)
		return minutes