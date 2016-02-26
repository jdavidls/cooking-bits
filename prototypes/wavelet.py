#!/usr/bin/env python


from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from time import sleep

from dsp import *

B = 256
fbank = FilterBank(B)


def draw_complex(data, p=0, w=1, f=abs):
	length = len(data)
	step = 2 / length

	glColor3f(1., 0., 0.)
	glBegin(GL_LINE_STRIP)
	for n in range(length):
		x = -1 + step * n
		y = p + data[n].real * w
		glVertex2f(x,y)
	glEnd()

	glColor3f(0., 0., 1.)
	glBegin(GL_LINE_STRIP)
	for n in range(length):
		x = -1 + step * n
		y = p + data[n].imag * w
		glVertex2f(x,y)
	glEnd()

	glColor3f(0., 1., 0.)
	glBegin(GL_LINE_STRIP)
	for n in range(length):
		x = -1 + step * n
		y = p + f(data[n]) * w
		glVertex2f(x,y)
	glEnd()



def display():
	glClear(GL_COLOR_BUFFER_BIT)

	glColor3f(.5, .5, .5)
	glBegin(GL_LINES)
	glVertex2f(-1,0)
	glVertex2f(+1,0)
	glEnd()

	draw_complex(fbank.wavelets[B>>1])


	glutSwapBuffers()


def keyboard(ascii, code, mod):
	if ascii == b'\x1b':
		glutLeaveMainLoop()

	glutPostRedisplay();


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow('Wavelet')
glClearColor(0., 0., 0., 1.)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
