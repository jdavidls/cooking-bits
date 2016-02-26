#!/usr/bin/env python

from glapplication import *
import np


grid = np.complex_grid()
grid2 = grid * grid
step_0 = 0.000000
delta_0 = 0.01

step = step_0
delta = delta_0

class App(GLApplication):
	def gl_init(self):
		glColor3f(.0, .9, .2)

	def render(self):
		global grid, step

#		np.draw_complex_grid(grid ** (grid*step) )
		np.draw_complex_grid(grid ** (grid*step) )

		step += delta

	def keyboard(self, key, x, y):
		global delta, delta_0
		if key == ' ':
			delta = delta_0 if delta == 0 else 0
		if key == 'b':
			delta_0 = -delta_0
			delta = -delta





if __name__ == '__main__':
	App().run()
