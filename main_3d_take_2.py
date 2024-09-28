# main_incl_visualization.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from simulation.engine import SimulationEngine
from config import Config
import logging
import math

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

agent_bounds = (100, 100)
engine = SimulationEngine(bounds=agent_bounds)
engine.initialize_agents_predefined_patterns()

engine.running = True
agents = engine.get_state()

def draw_cube(x, y, height, color):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(*color)
    
    vertices = [
        (0, 0, 0), (0.01, 0, 0), (0.01, 0.01, 0), (0, 0.01, 0),  # Bottom face
        (0, 0, height), (0.01, 0, height), (0.01, 0.01, height), (0, 0.01, height)  # Top face
    ]
    
    faces = [
        (0, 1, 2, 3),  # Bottom face
        (4, 5, 6, 7),  # Top face
        (0, 4, 7, 3),  # Left face
        (1, 5, 6, 2),  # Right face
        (0, 1, 5, 4),  # Front face
        (3, 2, 6, 7)   # Back face
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glPopMatrix()

camera_distance = 2.0
camera_height = 1.0
camera_angle = 0
pan_x, pan_y = 0, 0
zoom = 1.0

clock = pygame.time.Clock()
last_mouse_pos = None
mouse_button_down = False

while engine.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            engine.running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camera_angle -= 0.1
            elif event.key == pygame.K_RIGHT:
                camera_angle += 0.1
            elif event.key == pygame.K_UP:
                camera_height += 0.1
            elif event.key == pygame.K_DOWN:
                camera_height -= 0.1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_button_down = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4:  # Mouse wheel up
                zoom *= 1.1
            elif event.button == 5:  # Mouse wheel down
                zoom /= 1.1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_button_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_button_down:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]
                pan_x += dx * 0.001
                pan_y -= dy * 0.001
                last_mouse_pos = current_mouse_pos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45 / zoom, (display[0] / display[1]), 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    camera_x = camera_distance * math.sin(camera_angle)
    camera_z = camera_distance * math.cos(camera_angle)
    gluLookAt(camera_x, camera_height, camera_z,  # Camera position
              0.5 + pan_x, pan_y, 0.5,  # Look at point
              0, 1, 0)  # Up vector
    
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    
    alive_count = 0
    for agent in agents:
        if agent['state'] == 'alive':
            x, y = agent['position']
            x = x / agent_bounds[0]
            y = y / agent_bounds[1]
            color = agent['color'][agent['state']]
            height = max(0.001, agent['height'] * 0.1)  # Ensure minimum height
            
            draw_cube(x, y, height, color)
            alive_count += 1

    pygame.display.flip()
    
    engine.update()
    agents = engine.get_state()

    logging.debug(f"Alive agents: {alive_count}")

    clock.tick(30)  # Limit to 30 FPS

logging.info("Simulation ended")