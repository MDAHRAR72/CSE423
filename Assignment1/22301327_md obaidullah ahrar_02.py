from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

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
    
    # Convert window coordinates to OpenGL coordinates
    opengl_x = (x - w_width/2) * (box_right - box_left) / w_width
    opengl_y = ((w_height - y) - w_height/2) * (box_top - box_bottom) / w_height
    
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
    # Clear buffer
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Reset transformations
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Draw box and points
    draw_box()
    draw_all_points()
    
    # Swap buffers (double buffering)
    glutSwapBuffers()

def animate():
    # Update points' positions
    update_points()
    glutPostRedisplay()

def init():
    # Initialize OpenGL settings
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
    
    # Register callbacks
    init()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    
    # Start main loop
    glutMainLoop()

# Call main function
if __name__ == "__main__":
    main()