import revitron
import revitronui
import sqlite3
import json
from datetime import datetime
from pyrevit import script
from pyrevit import forms

def tableCell(text):
	return '<td style="white-space: nowrap; vertical-align: top; text-align: left; padding-right: 30px;">{}</td>'.format(str(text))

config = revitron.DocumentConfigStorage().get('revitron.history', dict())
sqliteFile = config.get('file', '')

if not sqliteFile:
	forms.alert('There hasn\'t been anything logged yet!', exitscript=True)

out = script.get_output()

try:
	conn = sqlite3.connect(sqliteFile)
	cursor = conn.cursor()
	users = ['*']
	cursor.execute("SELECT user FROM syncs GROUP BY user ORDER BY user COLLATE NOCASE ASC")
	rows = cursor.fetchall()
except:
	forms.alert('There hasn\'t been anything logged yet!', exitscript=True)

for row in rows:
	users.append(row[0])

userFilter = forms.SelectFromList.show(users, button_name='Filter by User')

out.print_md('Sync History for: **{}**<br>'.format(revitron.DOC.Title))

param = dict()
sql = "SELECT startTime, finishTime, size, user FROM syncs"

if userFilter != '*':
	sql += " WHERE user = :user"
	param = {'user': userFilter}

sql += " ORDER BY startTime DESC"

cursor.execute(sql, param)
rows = cursor.fetchmany(100)
cursor.close()
conn.close()

out.print_md('### Last 100 syncs')

table = '<table>'

table += '<tr>'
for title in ['Started', 'Duration', 'Size', 'User']:
	table += '<th style="font-weight: normal; text-align: left; color: #aaa;">{}</th>'.format(title)
table += '</tr>'

syncMinutes = []

for row in rows:
	table += '<tr>'
	table += tableCell(row[0])
	minutes = revitronui.Date.diff(row[0], row[1])
	syncMinutes.append(minutes)
	table += tableCell(str(minutes) + ' min')
	table += tableCell(str(round(float(str(row[2]).replace(' mb', '')), 2)) + ' mb')
	table += tableCell(row[3])
	table += '</tr>' 

table += '</table>'  

averageSyncTime = sum(syncMinutes) / float(len(syncMinutes))
out.print_md('**Average sync time is ' + str(averageSyncTime) + ' min**')
out.print_html(table)

