#!/usr/bin/env python



from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from time import sleep
from math import *

qua = .5 * pi
tau = 2. * pi
phi = (1 + sqrt(5)) * .5
cot = lambda x: 1 / tan(x)
exp = lambda x: e ** x


'''
T: periodo de oscilacion en samples (wavelength)
F: frecuencia angular

window(T,t) = cos(pi / T * t) + 1
osc(T,t) = e ** (i * tau / T * t)

wavelength(b) = 2(b+1)

'''


wavelength = lambda b: 2 * (b+1)
bandlength = lambda b: 2 * wavelength(b) + 1



window = lambda T,t: cos(pi / T * t) + 1
osc = lambda T,t: e ** (1j * tau / T * t)
osc_window = lambda T,t: window(T, t) * osc(T, t) * .5


def frame(b, F=osc_window):
	T = wavelength(b)
	return [ F(T, t-T) for t in range(bandlength(b))  ]




B = 128
current_band = B-1
current_band2 = B-1

bands = [ frame(b) for b in range(B) ]
spectrum = [complex() for b in range(B) ]

buffer_length = len(bands[-1])
buffer_center = ( buffer_length - 1 ) //  2

input = [ .0 for b in range(buffer_length)]
output = [ .0 for b in range(buffer_length)]

print('buffer length:', buffer_length)

def process(sample):
	input.pop(0)
	input.append(sample)

	out = .0
	for b in range(B):
		band = bands[b]
		offset = buffer_center - wavelength(b)

		acc = complex()
		for n in range(len(band)):
			acc += input[offset+n] * band[n]


		acc *= 1 / (b+1)

		spectrum[b] = acc
		# spectrum[h] *= 1 + abs(spectrum[b]) * exciter_coeff[h]


		out += acc / (b+1)

	#out /= B

	return out




phaser = .0
phaser2 = .0


def draw_complex(data, p, w, f=abs):
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
	global phaser, phaser2

	glClear(GL_COLOR_BUFFER_BIT)
	phaser += tau / wavelength(current_band)
	phaser2 += tau / wavelength(current_band2)

	out = process(cos(phaser))
	#out = process(.5*cos(phaser) + .5*cos(phaser2))
	#out = process(complex(.5*cos(phaser), .5*cos(phaser2)))

	output.pop(0)
	output.append(.0)
	output[buffer_center] = out


	## DRAW COMPLEX

	draw_complex(spectrum, .0, 1.)
	draw_complex(input, +.5, .4, lambda c: c.real + c.imag)
	draw_complex(output,-.5, .4, lambda c: c.real + c.imag)


	glColor3f(1., 1., 0.)
	glBegin(GL_LINES)
	step = 2 / B
	x = -1 + step * (current_band+.5)
	glVertex2f(x,-1)
	glVertex2f(x,1)
	x = -1 + step * (current_band2+.5)
	glVertex2f(x,-1)
	glVertex2f(x,1)

	glEnd()



	glutSwapBuffers()
	#sleep(0.1)
	glutPostRedisplay()


def display_hat():
	glClear(GL_COLOR_BUFFER_BIT)

	glColor3f(.5, .5, .5)
	glBegin(GL_LINES)
	glVertex2f(-1,0)
	glVertex2f(+1,0)
	glEnd()

	band = bands[current_band]
	step = 2 / len(band)

	glColor3f(0., 1., 0.)
	glBegin(GL_LINE_STRIP)
	for n in range(len(band)):
		x = -1 + step * (n+.5)
		y = band[n]
		glVertex2f(x,y.real)
	glEnd()

	glColor3f(0., 0., 1.)
	glBegin(GL_LINE_STRIP)
	for n in range(len(band)):
		x = -1 + step * (n+.5)
		y = band[n]
		glVertex2f(x,y.imag)
	glEnd()


	glutSwapBuffers()


def keyboard(ascii, code, mod):
	global current_band, current_band2

	if ascii == b'w' and current_band < B-1:
		current_band += 1
	elif ascii == b's' and current_band > 0:
		current_band -= 1

	if ascii == b'e' and current_band2 < B-1:
		current_band2 += 1
	elif ascii == b'd' and current_band2 > 0:
		current_band2 -= 1



	elif ascii == b'\x1b':
		glutLeaveMainLoop()
	else:
		print(ascii, code, mod)

	print('current_band', current_band, current_band2)
	#updateCamera()
	glutPostRedisplay();

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(800, 800)
	glutCreateWindow('spectra')

	glClearColor(0., 0., 0., 1.)
	#glShadeModel(GL_SMOOTH)
	#glEnable(GL_CULL_FACE)
	#glEnable(GL_DEPTH_TEST)

	#glPointSize(2);

	glutDisplayFunc(display)
	#glutDisplayFunc(display_hat)
	glutKeyboardFunc(keyboard)
	glutMainLoop()



main()
