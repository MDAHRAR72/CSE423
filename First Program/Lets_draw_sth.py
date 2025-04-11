from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Window dimensions
W_Width, W_Height = 500, 500

# Raindrop properties
raindrops = []
rain_speed = 2
rain_direction = 0  # 0 for straight, negative for left, positive for right

# Background color and transition properties
background_color = [0.0, 0.0, 0.0]  # Start with black (night)
transition_speed = 0.01  # Speed of color transition
target_color = [0.0, 0.0, 0.0]  # Target color for transition

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_house():
    # Roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.3, 0)
    glVertex2d(-150, 0)
    glVertex2d(150, 0)
    glVertex2d(0, 75)
    glEnd()

    # Walls
    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.7, 0.6)  # Beige
    glVertex2d(-125, 0)
    glVertex2d(-125, -100)
    glVertex2d(125, -100)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.7, 0.6)  # Beige
    glVertex2d(125, 0)
    glVertex2d(-125, 0)
    glVertex2d(125, -100)
    glEnd()

    # Door
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(-15, -100)
    glVertex2d(-15, -30)
    glVertex2d(15, -100)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(15, -30)
    glVertex2d(-15, -30)
    glVertex2d(15, -100)
    glEnd()

    # Windows
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(-90, -60)
    glVertex2d(-90, -30)
    glVertex2d(-65, -60)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(-65, -60)
    glVertex2d(-90, -30)
    glVertex2d(-65, -30)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(90, -60)
    glVertex2d(90, -30)
    glVertex2d(65, -60)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)  # Brown
    glVertex2d(65, -60)
    glVertex2d(90, -30)
    glVertex2d(65, -30)
    glEnd()

def create_raindrop():
    x = random.uniform(-250, 250)  # Random x-coordinate between -250 and 250
    y = 250  # Start at the top of the window
    raindrops.append([x, y])

def draw_raindrops():
    global raindrops, rain_direction
    glColor3f(0.53, 0.81, 0.92)
    for drop in raindrops:
        glColor3f(0.0, 0.5, 1.0)
        draw_points(drop[0], drop[1], 2)
        drop[0] += rain_direction  # Bend left or right
        drop[1] -= rain_speed  # Fall down
        if drop[1] < -250:  # Remove raindrop if it goes below the window
            raindrops.remove(drop)

def update_background_color():
    global background_color, target_color, transition_speed
    for i in range(3):  # Update each RGB component
        if background_color[i] < target_color[i]:
            background_color[i] += transition_speed
        elif background_color[i] > target_color[i]:
            background_color[i] -= transition_speed

def keyboardListener(key, x, y):
    global target_color
    if key == b'b':  # Change to light background (day)
        target_color = [1.0, 1.0, 1.0]  # White
    elif key == b'd':  # Change to dark background (night)
        target_color = [0.0, 0.0, 0.0]  # Black
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:  # Bend rain to the left
        rain_direction -= 0.1
    elif key == GLUT_KEY_RIGHT:  # Bend rain to the right
        rain_direction += 0.1
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 0)  # Set background color
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_house()
    draw_raindrops()

    glutSwapBuffers()

def animate():
    create_raindrop()  # Continuously create new raindrops
    update_background_color()  # Gradually update background color
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-250, 250, -250, 250)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Rainy House with Day-Night Cycle")

init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()