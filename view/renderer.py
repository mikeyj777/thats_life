# view/renderer.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from config import Config
import time

class Renderer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.width, self.height = Config.SIMULATION_PARAMS['resolution']
        self.cell_size = 1.0
        self.max_height = 1.0
        self.display = (800, 600)
        self.clock = pygame.time.Clock()

    def init_gl(self):
        print("Initializing OpenGL...")
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        print("OpenGL initialized.")

    def set_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.width/2, -self.height/2, self.width,
                  self.width/2, self.height/2, 0,
                  0, 0, 1)

    def draw_cell(self, x, y, agent):
        if agent is None or not self.simulation.is_alive(x, y):
            return

        glPushMatrix()
        glTranslatef(x * self.cell_size, y * self.cell_size, 0)
        
        glColor3f(*agent.color['alive'])

        height = agent.height * self.max_height
        glBegin(GL_QUADS)
        # Bottom face
        glVertex3f(0, 0, 0)
        glVertex3f(self.cell_size, 0, 0)
        glVertex3f(self.cell_size, self.cell_size, 0)
        glVertex3f(0, self.cell_size, 0)
        # Top face
        glVertex3f(0, 0, height)
        glVertex3f(self.cell_size, 0, height)
        glVertex3f(self.cell_size, self.cell_size, height)
        glVertex3f(0, self.cell_size, height)
        # Side faces
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, height)
        glVertex3f(self.cell_size, 0, height)
        glVertex3f(self.cell_size, 0, 0)
        glEnd()

        glPopMatrix()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.set_camera()

        for i in range(self.width):
            for j in range(self.height):
                agent = self.simulation.get_agent(i, j)
                self.draw_cell(i, j, agent)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def start(self):
        self.init_gl()
        running = True
        frame_count = 0
        start_time = time.time()

        while running:
            running = self.handle_events()
            
            update_start = time.time()
            print(f'update start {update_start}')
            self.simulation.update()
            update_end = time.time()
            print(f"Update time: {(update_end - update_start) * 1000:.2f}ms")
            
            render_start = time.time()
            self.render()
            render_end = time.time()
            
            frame_count += 1
            if frame_count % 60 == 0:
                end_time = time.time()
                print(f"FPS: {frame_count / (end_time - start_time):.2f}")
                print(f"Update time: {(update_end - update_start) * 1000:.2f}ms")
                print(f"Render time: {(render_end - render_start) * 1000:.2f}ms")
                frame_count = 0
                start_time = end_time

            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        print("Renderer stopped.")