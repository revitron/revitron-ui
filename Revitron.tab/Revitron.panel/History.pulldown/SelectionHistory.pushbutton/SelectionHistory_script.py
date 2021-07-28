import revitron
import sqlite3
import json
from pyrevit import script
from pyrevit import forms


def tableCell(text):
	return '<td style="white-space: nowrap; vertical-align: top; text-align: left; padding-right: 30px;">{}</td>'.format(
	    text
	)


config = revitron.DocumentConfigStorage().get('revitron.history', dict())
sqliteFile = config.get('file', '')
selection = revitron.Selection.get()

if not sqliteFile:
	forms.alert('Logging is disabled for this Revit model!', exitscript=True)

if not selection:
	forms.alert('Nothing Selected!', exitscript=True)

out = script.get_output()

sqlTransactions = "SELECT transactions, syncId FROM transactions WHERE elementId = :id ORDER BY syncId DESC"
sqlSync = "SELECT startTime, user FROM syncs WHERE syncId = :id"

out.print_md('Open Log for: **{}**<br>'.format(revitron.DOC.Title))

for element in selection:

	out.print_html('<hr style="border: none; border-bottom: 1px dotted #ccc;" />')

	info = ''
	try:
		if element.Category is not None:
			info += element.Category.Name + ' '
	except:
		pass
	try:
		if element.Name is not None:
			info += element.Name + ' '
	except:
		pass

	info += revitron.Parameter(element, 'Family and Type').getValueString()
	out.print_md('###' + info.strip() + ' ' + out.linkify(element.Id))

	try:
		conn = sqlite3.connect(sqliteFile)
		cursor = conn.cursor()
		cursor.execute(sqlTransactions, {'id': element.Id.ToString()})
		rows = cursor.fetchall()
	except:
		out.close()
		forms.alert('There hasn\'t been anything logged yet!', exitscript=True)

	if rows:

		table = '<table>'
		table += '<tr>'
		table += '<th style="font-weight: normal; text-align: left; color: #aaa;">Synced</th>'
		table += '<th style="font-weight: normal; text-align: left; color: #aaa;">User</th>'
		table += '<th style="width: 100%; font-weight: normal; text-align: left; color: #aaa;">Transactions</th>'
		table += '</tr>'

		for row in rows:
			cursor.execute(sqlSync, {'id': row[1]})
			syncs = cursor.fetchall()
			sync = syncs[0]
			table += '<tr>'
			# Sync
			table += tableCell(sync[0])
			# User
			table += tableCell(sync[1])
			# Transactions
			transactions = json.loads(row[0])
			table += tableCell(',<br>'.join(list(reversed(transactions))))
			table += '</tr>'

		table += '</table>'
		out.print_html(table)

	else:

		out.print_md('**This element has no history yet.**')

	out.print_html('<br>')
