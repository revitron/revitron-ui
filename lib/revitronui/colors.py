class Palette:

	def __init__(self, steps, colorA='ffffff', colorB='2c3e50'):
		self.colors = []
		for i in range(0, steps):
			perc = (i + 1) * 100.0 / steps
			self.colors.append(self.mix(colorA, colorB, perc))

	def get(self):
		return self.colors

	def mix(self, colorA, colorB, perc):
		factorA = ((100.0 - perc) / 100.0)
		factorB = (perc / 100.0)
		redA = int(int(colorA[:2], 16) * factorA)
		redB = int(int(colorB[:2], 16) * factorB)
		greenA = int(int(colorA[2:4], 16) * factorA)
		greenB = int(int(colorB[2:4], 16) * factorB)
		blueA = int(int(colorA[4:6], 16) * factorA)
		blueB = int(int(colorB[4:6], 16) * factorB)
		red = redA + redB
		green = greenA + greenB
		blue = blueA + blueB
		return '#{}{}{}'.format(
		    self.zpad(hex(red)[2:]), self.zpad(hex(green)[2:]), self.zpad(hex(blue)[2:])
		)

	def zpad(self, x):
		if len(x) == 2:
			return x
		return '0' + x
