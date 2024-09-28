# backend/renderer.py

import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy as np
from config import Config

class Renderer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.width = Config.SIMULATION_PARAMS['width']
        self.height = Config.SIMULATION_PARAMS['height']
        self.cell_size = 1.0
        self.max_height = 1.0

    def init_gl(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(800, 600)
        glut.glutCreateWindow(b"Game of Life 3D")

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

    def set_camera(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(45, 800/600, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluLookAt(self.width/2, -self.height/2, self.width,
                     self.width/2, self.height/2, 0,
                     0, 0, 1)

    def draw_cell(self, x, y, agent):
        if agent is None or agent.state == 'dead':
            return

        gl.glPushMatrix()
        gl.glTranslatef(x * self.cell_size, y * self.cell_size, 0)
        gl.glColor3fv(agent.color['alive'])

        # Draw the cell as a rectangular prism
        gl.glBegin(gl.GL_QUADS)
        # Bottom face
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(self.cell_size, 0, 0)
        gl.glVertex3f(self.cell_size, self.cell_size, 0)
        gl.glVertex3f(0, self.cell_size, 0)
        # Top face
        height = agent.height * self.max_height
        gl.glVertex3f(0, 0, height)
        gl.glVertex3f(self.cell_size, 0, height)
        gl.glVertex3f(self.cell_size, self.cell_size, height)
        gl.glVertex3f(0, self.cell_size, height)
        # Side faces
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, 0, height)
        gl.glVertex3f(self.cell_size, 0, height)
        gl.glVertex3f(self.cell_size, 0, 0)
        gl.glVertex3f(self.cell_size, 0, 0)
        gl.glVertex3f(self.cell_size, 0, height)
        gl.glVertex3f(self.cell_size, self.cell_size, height)
        gl.glVertex3f(self.cell_size, self.cell_size, 0)
        gl.glVertex3f(self.cell_size, self.cell_size, 0)
        gl.glVertex3f(self.cell_size, self.cell_size, height)
        gl.glVertex3f(0, self.cell_size, height)
        gl.glVertex3f(0, self.cell_size, 0)
        gl.glVertex3f(0, self.cell_size, 0)
        gl.glVertex3f(0, self.cell_size, height)
        gl.glVertex3f(0, 0, height)
        gl.glVertex3f(0, 0, 0)
        gl.glEnd()

        gl.glPopMatrix()

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.set_camera()

        for i in range(self.width):
            for j in range(self.height):
                agent = self.simulation.agents[i, j]
                self.draw_cell(i, j, agent)

        glut.glutSwapBuffers()

    def start(self):
        self.init_gl()
        glut.glutDisplayFunc(self.render)
        glut.glutIdleFunc(self.simulation.update)
        glut.glutMainLoop()