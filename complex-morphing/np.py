from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from numpy import *


def complex_grid(res=20, rad=1.0, nozero=0):
    radres = rad/res
    def gen(x,y):
        return (.5+x-res) * radres + (.5+y-res) * radres * 1j
    return fromfunction(gen, (res*2, res*2), dtype=complex)

def draw_complex_grid(grid):
	length = len(grid[0])

	for row in range(length):
		draw_complex_path(grid[row])

	for col in range(length):
		draw_complex_path(grid[:,col])

def draw_complex_path(path):
	glBegin(GL_LINE_STRIP)
	for val in path:
		glVertex2f(val.real, val.imag)
	glEnd()
