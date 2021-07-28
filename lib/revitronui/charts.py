from pyrevit import script


class LineChart:

	def __init__(self, data, labels, title=None):
		import revitronui
		self.output = script.get_output()
		self.chart = self.make()
		self.chart.data.labels = labels
		dataset = self.chart.data.new_dataset(title)
		dataset.data = data
		if self.hasBackground:
			palette = revitronui.Palette(len(data))
			dataset.backgroundColor = palette.get()
		else:
			dataset.set_color(0x2c, 0x3e, 0x50, 0.5)
		if title:
			self.chart.options.title = {
			    'display': True,
			    'text': title,
			    'fontSize': 18,
			    'fontColor': '#2c3e50',
			    'fontStyle': 'bold'
			}

	@property
	def hasBackground(self):
		return False

	def make(self):
		return self.output.make_line_chart()

	def draw(self):
		self.chart.draw()

	def get(self):
		return self.chart


class BarChart(LineChart):

	def make(self):
		return self.output.make_bar_chart()


class DoughnutChart(LineChart):

	@property
	def hasBackground(self):
		return True

	def make(self):
		return self.output.make_doughnut_chart()


class PieChart(DoughnutChart):

	def make(self):
		return self.output.make_pie_chart()