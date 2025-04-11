import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

w_width, w_height = 800, 600

# For changing background color
background_color = [0.0, 0.0, 0.0]
transition_speed = 0.01
transition = 0.5
target_color = [0.0, 0.0, 0.0]

# Rain properties
rain_angle = 0.0
rain_speed = 10
raindrops = []


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Creater the house


def draw_house():
    # rooft
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)
    glVertex2d(-750, 0)
    glVertex2d(750, 0)
    glVertex2d(0, 375)
    glEnd()

    # wallt1
    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2d(-725, 0)
    glVertex2d(-725, -500)
    glVertex2d(725, -500)
    glEnd()

    # wallt2
    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.7, 0.6)
    glVertex2d(725, 0)
    glVertex2d(-725, 0)
    glVertex2d(725, -500)
    glEnd()

    # doort1
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(-75, -500)
    glVertex2d(-75, -150)
    glVertex2d(75, -500)
    glEnd()

    # doort2
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(75, -150)
    glVertex2d(-75, -150)
    glVertex2d(75, -500)
    glEnd()

    # window1t1
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(-450, -300)
    glVertex2d(-450, -150)
    glVertex2d(-325, -300)
    glEnd()

    # window1t2
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(-325, -300)
    glVertex2d(-450, -150)
    glVertex2d(-325, -150)
    glEnd()

    # window2t1
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(450, -300)
    glVertex2d(450, -150)
    glVertex2d(325, -300)
    glEnd()

    # window2t2
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.2, 0.0)
    glVertex2d(325, -300)
    glVertex2d(450, -150)
    glVertex2d(325, -150)
    glEnd()

# Appending the raindrops


def create_raindrop():
    x = random.uniform(-1920, 1920)
    y = 1080
    raindrops.append([x, y])

# Dropping raindrops


def draw_raindrops():
    global raindrops, rain_angle
    glColor3f(0.0, 0.0, 1.0)  # Set raindrop color to sky blue
    glLineWidth(2)  # Set the thickness of the raindrops
    for drop in raindrops:
        glBegin(GL_LINES)
        glVertex2f(drop[0], drop[1])  # Top of the raindrop
        # Bottom of the raindrop (10 pixels long)
        glVertex2f(drop[0], drop[1] - 30)
        glEnd()
        # Update raindrop position
        drop[0] += rain_angle  # Bend left or right
        drop[1] -= rain_speed  # Fall down
        if drop[1] < -1080:  # Remove raindrop if it goes below the window
            raindrops.remove(drop)


def update_background_color():
    global background_color, target_color, transition_speed
    for i in range(3):  # Update each RGB component
        if background_color[i] < target_color[i]:
            background_color[i] += transition_speed
        elif background_color[i] > target_color[i]:
            background_color[i] -= transition_speed


def keyboardListener(key, x, y):
    global transition, transition_speed
    if key == b'd':
        transition = min(1.0, transition + transition_speed)
    elif key == b'n':
        transition = max(0.0, transition - transition_speed)
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global rain_angle
    if key == GLUT_KEY_LEFT:
        rain_angle -= 0.2
    elif key == GLUT_KEY_RIGHT:
        rain_angle += 0.2
    elif key == b'\x1b':  # ESC key
        glutLeaveMainLoop()
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    day = [1.0, 1.0, 1.0]
    night = [0.0, 0.0, 0.0]
    background_color[0] = night[0] + (day[0] - night[0]) * transition
    background_color[1] = night[1] + (day[1] - night[1]) * transition
    background_color[2] = night[2] + (day[2] - night[2]) * transition

    draw_house()
    draw_raindrops()
    glutSwapBuffers()


def animate():
    create_raindrop()  # THis will create new raindrops
    update_background_color()  # Pressing B and D update background color
    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1920, 1920, -1080, 1080)


glutInit()
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"House in Rainfall")

init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()


######################################### TASK 2 ################################################


# Window dimensions
w_width, w_height = 800, 600

# Box boundary
box_left = -600
box_right = 600
box_bottom = -400
box_top = 400

# Points properties
points = []  # [x, y, dx, dy, r, g, b, blinking, blink_state, last_blink_time]
point_size = 8.0
point_speed_multiplier = 1.0
is_frozen = False
is_blinking = False


def draw_points(x, y, size, r, g, b):
    glPointSize(size)
    glColor3f(r, g, b)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_box():
    # Draw the boundary box
    glColor3f(1.0, 1.0, 1.0)  # White color
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box_left, box_bottom)
    glVertex2f(box_right, box_bottom)
    glVertex2f(box_right, box_top)
    glVertex2f(box_left, box_top)
    glEnd()


def create_point(x, y):
    r = random.random()
    g = random.random()
    b = random.random()

    dx = random.uniform(1.0, 3.0) * random.choice([-1, 1])
    dy = random.uniform(1.0, 3.0) * random.choice([-1, 1])

    points.append([x, y, dx, dy, r, g, b, False, 1, time.time()])


def update_points():
    global points, point_speed_multiplier

    if is_frozen:
        return

    current_time = time.time()

    for point in points:
        x, y, dx, dy, r, g, b, blinking, blink_state, last_blink_time = point

        x += dx * point_speed_multiplier
        y += dy * point_speed_multiplier

        if x <= box_left or x >= box_right:
            dx = -dx
            x += dx * point_speed_multiplier  # Prevent sticking to wall

        if y <= box_bottom or y >= box_top:
            dy = -dy
            y += dy * point_speed_multiplier  # Prevent sticking to wall

        # Ttoggle visibility every 500 miliseconds
        if blinking and current_time - last_blink_time >= 0.5:
            blink_state = 1 - blink_state  # BLINK
            last_blink_time = current_time

        point[0] = x
        point[1] = y
        point[2] = dx
        point[3] = dy
        point[8] = blink_state
        point[9] = last_blink_time


def draw_all_points():
    for point in points:
        x, y, dx, dy, r, g, b, blinking, blink_state, last_blink_time = point

        # If point is blinking and currently in invisible state (blink_state = 0),
        # skip drawing it
        if blinking and blink_state == 0:
            continue

        draw_points(x, y, point_size, r, g, b)


def mouseListener(button, state, x, y):
    global is_blinking

    if is_frozen:
        return
    opengl_x = (x - w_width/2) * (box_right - box_left) / w_width
    opengl_y = ((w_height - y) - w_height/2) * \
        (box_top - box_bottom) / w_height

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_point(opengl_x, opengl_y)

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        is_blinking = not is_blinking
        for point in points:
            point[7] = is_blinking

    glutPostRedisplay()


def keyboardListener(key, x, y):
    global is_frozen

    if key == b' ':  # Spacebar
        # Toggle freeze state
        is_frozen = not is_frozen

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global point_speed_multiplier

    if is_frozen:
        return

    if key == GLUT_KEY_UP:
        # Increase speed
        point_speed_multiplier += 0.2
    elif key == GLUT_KEY_DOWN:
        # Decrease speed, but keep it above 0
        point_speed_multiplier = max(0.2, point_speed_multiplier - 0.2)

    glutPostRedisplay()


def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_box()
    draw_all_points()

    glutSwapBuffers()


def animate():
    update_points()
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(box_left, box_right, box_bottom, box_top)

# Main function


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w_width, w_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Amazing Box")

    init()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)

    glutMainLoop()


if __name__ == "__main__":
    main()
