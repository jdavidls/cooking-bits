#!/usr/bin/env python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from dsp import *


PHASORS = 10
FILTERS = 256

selected = 0



phasors = PhasorBank(PHASORS)
filters = FilterBank(FILTERS)

output = [ complex() for _ in range(filters.window_length) ]


oscillators = [ int(n * FILTERS / PHASORS) for n in range(PHASORS) ]
oscillators[0] = FILTERS-1

for n in range(PHASORS):
	phasors.velocities[n] = tau / filters.wavelength(oscillators[n])
	phasors.amplitudes[n] = .0

phasors.amplitudes[0] = .5


oscillators[PHASORS//3] = oscillators[0] //3
phasors.phases[PHASORS//3] = pi
phasors.velocities[PHASORS//3] = 3 * tau / filters.wavelength(oscillators[0])
phasors.amplitudes[PHASORS//3] = .0

filter_solo = False


def draw_complex(data, p, w, f=abs):
	length = len(data)
	step = 2 / length


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

	glColor3f(1., 0., 0.)
	glBegin(GL_LINE_STRIP)
	for n in range(length):
		x = -1 + step * n
		y = p + data[n].real * w
		glVertex2f(x,y)
	glEnd()



def display():
	global phaser, phaser2

	glClear(GL_COLOR_BUFFER_BIT)

	sample = phasors()

	out = filters(sample.real)

	output.pop(0)
	output.append(.0)

	if filter_solo:
		out = filters.spectrum[oscillators[selected]]
	output[filters.center_offset] = out

	## DRAW COMPLEX

	draw_complex(filters.spectrum, .0, 1.)
	draw_complex(filters.buffer, +.5, .5)#, lambda c: c.real + c.imag)
	draw_complex(output,-.5, .5, lambda c: c.real + c.imag)



	glBegin(GL_LINES)
	for n in range(PHASORS):
		if n == selected:
			if filter_solo:
				glColor3f(1., 1., 0.)
			else:
				glColor3f(.5, .5, 0.)
		else:
			glColor3f(.3, .3, .3)

		step = 2 / FILTERS
		x = -1 + step * (oscillators[n]+.5)
		glVertex2f(x,-1)
		glVertex2f(x,1)
	glEnd()



	glutSwapBuffers()
	#sleep(0.1)
	glutPostRedisplay()


def update_velocity(amount):
	oscillator = oscillators[selected]

	oscillator += amount

	if oscillator < 0:
		oscillator = 0
	elif oscillator >= FILTERS:
		oscillator = FILTERS - 1

	oscillators[selected] = oscillator
	wavelength = filters.wavelength(oscillator)
	phasors.velocities[selected] = tau / filters.wavelength(oscillator)
	print('phasor', selected, 'exites filter', oscillator, '(tau/', wavelength, ')')

def update_amplitude(amount):
	amplitude = phasors.amplitudes[selected]

	amplitude += amount

	if amplitude > .5:
		amplitude = .5
	elif amplitude < 0:
		amplitude = 0.

	phasors.amplitudes[selected] = amplitude
	print('phasor', selected, 'has amplitude', amplitude)


def keyboard(key, x, y):
	global selected, filter_solo
	if key == b'\x1b':
	 	glutLeaveMainLoop()

	elif type(key) is bytes and key >= b'0' and key <= b'9':
	 	selected = int(key.decode('ascii'))
	 	print('selected', selected)


	elif key == GLUT_KEY_UP:
		update_amplitude(+.05)
	elif key == GLUT_KEY_DOWN:
		update_amplitude(-.05)
	elif key == GLUT_KEY_LEFT:
		update_velocity(-1)
	elif key == GLUT_KEY_RIGHT:
		update_velocity(1)

	elif key == b's':
		filter_solo = not filter_solo
		print('filter_solo', filter_solo)

	else:
		print('keyboard', key)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow(__file__)
glClearColor(0., 0., 0., 1.)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboard)
glutMainLoop()
