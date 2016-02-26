from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import time

class GLApplication:
	window_size = 800, 800
	window_buffer = GLUT_DOUBLE | GLUT_RGB
	window_title = __file__

	def __init__(self):
		self.glut_init()
		self.gl_init()

	def glut_init(self):
		glutInit(sys.argv)
		glutInitDisplayMode(self.window_buffer)
		glutInitWindowSize(*self.window_size)
		glutCreateWindow(self.window_title)
		glutDisplayFunc(self._render)
		glutKeyboardFunc(self._keyboard)
		glutSpecialFunc(self._keyboard)

	def gl_init(self):
		glClearColor(0., 0., 0., 1.)

	def run(self):
		glutMainLoop()

	def _render(self):
		glClear(GL_COLOR_BUFFER_BIT)

		self.render()

		glutSwapBuffers()

		time.sleep(0.01)
		glutPostRedisplay()

	def render(self):
		...

	def _keyboard(self, key, x, y):
		if key == b'\x1b':
		 	self.quit()

		elif type(key) is bytes:
		 	key = key.decode('ascii')

		print('key', key, ord(key) if isinstance(key, str) else None,  x, y)
		self.keyboard(key, x ,y)

	def keyboard(self, key, x, y):
		...

	def quit(self):
		 	glutLeaveMainLoop()
