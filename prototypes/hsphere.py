#!/usr/bin/env python


from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

tau = 2 * pi
phi = (1 + sqrt(5)) * .5
cot = lambda x: 1 / tan(x)

name = 'sphere of life'

class vec(tuple):
	def __new__(cls, x=.0, y=.0, z=.0):
		return tuple.__new__(cls, (float(x), float(y), float(z)))

	x = property(lambda v: v[0])
	y = property(lambda v: v[1])
	z = property(lambda v: v[2])

	__abs__ = lambda v: sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
	__neg__ = lambda v: v.__class__(-v.x, -v.y, -v.z)
	__add__ = lambda a, b: a.__class__(a.x + b.x, a.y + b.y, a.z + b.z)
	__sub__ = lambda a, b: a.__class__(a.x - b.x, a.y - b.y, a.z - b.z)
	__mul__ = lambda a, b: a.__class__(a.x * b.x, a.y * b.y, a.z * b.z)

	scale = lambda v, s: v.__class__(v.x * s, v.y * s, v.z * s)
	normalized = property(lambda v: v.scale(1 / abs(v)))

	def rotate(self, axis, radians):
		v = self
		r = mat.rotation(axis, radians)

		return vec(v.x * r.u.x + v.y * r.u.y + v.z * r.u.z,
					v.x * r.v.x + v.y * r.v.y + v.z * r.v.z,
					v.x * r.w.x + v.y * r.w.y + v.z * r.w.z)


class mat(tuple):
	def __new__(cls, u=(), v=(), w=()):
		return tuple.__new__(cls, (vec(*u), vec(*v), vec(*w)))

	u = property(lambda v: v[0])
	v = property(lambda v: v[1])
	w = property(lambda v: v[2])

	@classmethod
	def rotation(cls, u, r):
		x, y, z = vec(*u).normalized
		c, s = cos(r), sin(r)
		_1_c = 1 - c
		return cls(
			(c + x * x * _1_c, x * y * _1_c - z * s, x * z * _1_c + y * s),
			(y * x * _1_c + z * s, c + y * y * _1_c, y * z * _1_c - x * s),
			(z * x * _1_c - y * s, z * y * _1_c + x * s, c + z * z * _1_c),
		)

class quat(tuple):
	def __new__(cls, x=.0, y=.0, z=.0, w=.0):
		return tuple.__new__(cls, (float(x), float(y), float(z), float(w)))

	x = property(lambda s: s[0])
	y = property(lambda s: s[1])
	z = property(lambda s: s[2])
	w = property(lambda s: s[3])

	@classmethod
	def fromAxis(cls, axis, radians=.0):
		axis = axis.normalized
		radians = radians * .5
		s, c = sin(radians), cos(radians)
		return cls(axis.x * s, axis.y * s, axis.z * s, c)


	__abs__ = lambda v: sqrt(v.x * v.x + v.y * v.y + v.z * v.z + v.w * v.w)
	__neg__ = lambda v: v.__class__(-v.x, -v.y, -v.z, v.w)

	normalized = property(lambda v: v.scale(1 / abs(v)))

	__mul__ = lambda a, b: quat(a.w * b.x + a.x * b.w + a.y * b.z - b.z * a.y,
								a.w * b.y + a.y * b.w + a.z * b.x - a.x * b.z,
								a.w * b.z + a.z * b.w + a.x * b.y - a.y * b.x,
								a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z)



Origin = vec(0, 0, 0)
X_axis = vec(1, 0, 0)
Y_axis = vec(0, 1, 0)
Z_axis = vec(0, 0, 1)
step = tau / 60

camera = Z_axis.scale(5)
camera_v = Y_axis
camera_h = X_axis



def _xrange(begin, end, step):
	current = begin
	while current < end:
		yield current
		current += step

class Pointer:
	def __init__(self, position=Z_axis, direction=X_axis):
		self.position = position
		self.direction = direction
		self.step = tau / 100

	def advance(self, angular_distance=tau / 24):
		self.position = self.position.rotate(self.direction, angular_distance)
		return self

	def draw(self, angular_distance):
		if angular_distance < 0:
			return self
		elif angular_distance > tau:
			angular_distance = tau


		glBegin(GL_LINE_STRIP)
		for delta in _xrange(.0, angular_distance, self.step):
			v = self.position.rotate(self.direction, delta)
			glVertex3fv(v)

		v = self.position.rotate(self.direction, angular_distance).normalized
		glVertex3fv(v)
		self.position = v
		glEnd()

		return self

	def rotate(self, rads):
		self.direction = self.direction.rotate(self.position, rads)
		return self


	def angle(self, rads):
		return self.rotate(pi - rads)

	def copy(self):
		return Pointer(self.position, self.direction)


def solveTriangle(a, BC):
	'Two equal sides and the included angle given'
	A = acos(cos(BC) * cos(BC) + sin(BC) * sin(BC) * cos(a))

	bc = atan2(2 * sin(BC),
	#	 		  ---------------------------
					tan(a / 2) * sin(BC + BC))
	return A, bc

def drawPoligon(center, sides, radius):
	' Draws spherical polygon centered at center pointer '
	p = center.copy()
	a = tau / sides
	r = radius
	d, g = solveTriangle(a, r)

	p.advance(r).angle(g)

	for n in range(sides):
		p.draw(d).angle(2 * g)


def solveTriangle_3anglesGiven(a, b, c):
	A = acos((cos(a) + cos(b) * cos(c)) 	 /
	#		 	 -----------------------------
				 (sin(b) * sin(c)))

	return A, 0, 0



def drawThetrahedron(center=Pointer()):
	v = center.copy()
	A, B, C = solveTriangle_3anglesGiven(tau / 3, tau / 3, tau / 3)

	v.draw(A).angle(tau / 3).draw(A).angle(tau / 3).draw(A)
	v.angle(-tau / 3).draw(A).angle(-tau / 3).draw(A)
	v.angle(tau / 3).draw(A).angle(tau / 3).draw(A)
	v.angle(-tau / 3).draw(A).angle(-tau / 3).draw(A)

	# A/3



def drawLife():
	center = Pointer()

	# drawThetrahedron(center.copy().advance(pi))
	# drawThetrahedron(center)

	angleB = (phi) * tau
	angleA = (phi - 1) * tau


	p = center.copy()
	for x in range(50):
		p.rotate(angleA).draw(angleB)



	# drawPoligon(center.copy().rotate(tau / 12), 6, 1)
	# drawPoligon(center.copy().rotate(tau / 12).advance(pi / 4), 6, 0.5)
	# drawThetrahedron(center.rotate(pi))



#
# 	glColor3f(0, 1, 0)
#
# 	for n in range(3):
# 		v = Pointer().rotate(tau / 6 + n * tau / 3).advance(tau / 12)
# 		v.draw(A).angle(tau / 3).draw(A).angle(tau / 3).draw(A)
# 		v.angle(-tau / 3).draw(A).angle(-tau / 3).draw(A)
# 		v.angle(tau / 3).draw(A).angle(tau / 3).draw(A)
# 		v.angle(-tau / 3).draw(A).angle(-tau / 3).draw(A)


#
# 	glColor3f(0,0,1)
# 	v = Pointer().rotate(3*tau/6).advance(tau/9)
# 	v.draw(A).angle(tau/3).draw(A).angle(tau/3).draw(A)
# 	v.angle(-tau/3).draw(A).angle(-tau/3).draw(A)
# 	v.angle(tau/3).draw(A).angle(tau/3).draw(A)
# 	v.angle(-tau/3).draw(A).angle(-tau/3).draw(A)
#
# 	glColor3f(1,1,0)
# 	v = Pointer().rotate(5*tau/6).advance(tau/9)
# 	v.draw(A).angle(tau/3).draw(A).angle(tau/3).draw(A)
# 	v.angle(-tau/3).draw(A).angle(-tau/3).draw(A)
# 	v.angle(tau/3).draw(A).angle(tau/3).draw(A)
# 	v.angle(-tau/3).draw(A).angle(-tau/3).draw(A)



def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glPushMatrix()
	color = [0.3, 0.3, 0.5, 1.]
	glEnable(GL_LIGHTING)
	glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
	glutSolidSphere(0.99, 20, 20)
	glDisable(GL_LIGHTING)



	glColor3f(1, 1, 1)

	drawLife()

	glBegin(GL_LINES)
	glColor3f(1, 0, 0)
	glVertex3fv(Origin)
	glVertex3fv(X_axis.scale(5))

	glColor3f(0, 1, 0)
	glVertex3fv(Origin)
	glVertex3fv(Y_axis.scale(5))

	glColor3f(0, 0, 1)
	glVertex3fv(Origin)
	glVertex3fv(Z_axis.scale(5))

	glEnd()


	glPopMatrix()
	glutSwapBuffers()
	glutPostRedisplay();


def updateCamera():

	glLoadIdentity()
	gluLookAt(camera.x, camera.y, camera.z,
			  0, 0, 0,
			  camera_v.x, camera_v.y, camera_v.z)

def rotateCameraH(rads):
	global camera, camera_v
	camera = camera.rotate(camera_h, rads)
	camera_v = camera_v.rotate(camera_h, rads)

def rotateCameraV(rads):
	global camera, camera_h
	camera = camera.rotate(camera_v, rads)
	camera_h = camera_h.rotate(camera_v, rads)


def keyboard(ascii, code, mod):
	if ascii == b'w':
		rotateCameraH(-step)
	elif ascii == b's':
		rotateCameraH(step)
	elif ascii == b'd':
		rotateCameraV(step)
	elif ascii == b'a':
		rotateCameraV(-step)
	elif ascii == b'\x1b':
		glutLeaveMainLoop()
	else:
		print(ascii, code, mod)

	updateCamera()
	glutPostRedisplay();

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 800)
	glutCreateWindow(name)

	glClearColor(0., 0., 0., 1.)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_CULL_FACE)
	glEnable(GL_DEPTH_TEST)

	lightZeroPosition = [10., 4., 10., 1.]
	lightZeroColor = [1.0, 1.0, 1.0, 1.0]  # green tinged
	glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glEnable(GL_LIGHT0)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(40., 1., 1., 40.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(camera.x, camera.y, camera.z,
			  0, 0, 0,
			  camera_v.x, camera_v.y, camera_v.x)
	# glPushMatrix()

	glPointSize(2);

	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutMainLoop()
	return




if __name__ == '__main__': main()
