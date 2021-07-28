from pyrevit import forms


class Alert:

	def __init__(self, text):
		forms.alert(text, title='Note', ok=True, exitscript=True)