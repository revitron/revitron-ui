import revitron
import revitronui
import sqlite3
import pyrevit

config = revitron.DocumentConfigStorage().get('revitron.history', dict())
sqliteFile = config.get('file', '')
output = pyrevit.output.get_output()


def flexCharts(charts):
	nodes = []
	scripts = []
	for chart in charts:
		chart._setup_charts()
		canvasId = chart._make_canvas_unique_id()
		nodes.append(chart._make_canvas_code(canvasId))
		scripts.append(chart._make_charts_script(canvasId))
	output.print_html('<r-flex>{}</r-flex>'.format(''.join(nodes)))
	for script in scripts:
		output.inject_script(script, body=True)


if not sqliteFile:
	revitronui.Alert('Logging is disabled for this model!')

try:

	output.print_html('<h1>Model Stats for {}</h1>'.format(revitron.DOC.Title))
	output.add_style('body { padding: 50px; }')

	output.inject_to_head(
	    'link',
	    '',
	    {
	        'href': 'file:///{}'.format(__file__.replace('_script.py',
	                                                     '.css')),
	        'rel': 'stylesheet'
	    }
	)

	conn = sqlite3.connect(sqliteFile)
	cursor = conn.cursor()
	cursor.execute('SELECT size, finishTime, user FROM syncs')
	rows = cursor.fetchmany(100)
	sizes = [round(i[0], 2) for i in rows]
	users = ['{}, {}'.format(i[1], i[2]) for i in rows]
	sizeChart = revitronui.LineChart(sizes, users, 'File Size (MB)')
	sizeChart.draw()

	output.print_html('<br>')

	conn = sqlite3.connect(sqliteFile)
	cursor = conn.cursor()
	cursor.execute('SELECT startTime, finishTime, user FROM syncs')
	rows = cursor.fetchmany(100)
	times = [revitron.Date.diffMin(i[0], i[1]) for i in rows]
	users = [i[2] for i in rows]
	timeChart = revitronui.LineChart(times, users, 'Sync Time (MIN)')
	timeChart.draw()

	output.print_html('<br>')

	cursor.execute(
	    """SELECT syncs.user, count(*) 
		FROM syncs, transactions 
		WHERE syncs.syncId=transactions.syncId
		GROUP BY syncs.user"""
	)
	rows = cursor.fetchall()
	users = [i[0] for i in rows]
	count = [i[1] for i in rows]
	transactionChart = revitronui.DoughnutChart(count, users, 'Transactions by User')

	cursor.execute('SELECT user, count(*) FROM syncs GROUP BY user')
	rows = cursor.fetchall()
	users = [i[0] for i in rows]
	count = [i[1] for i in rows]
	syncsChart = revitronui.DoughnutChart(count, users, 'Syncs by User')

	conn.close()

	flexCharts([transactionChart.get(), syncsChart.get()])

except:
	revitronui.Alert('There hasn\'t been anything logged yet!')
