from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initial position of the square
catcher_x = 0
catcher_y = -0.8
catcher_width = 0.4
catcher_height = 0.1
catcher_shift = 0.03
catcher_color = [1.0, 1.0, 1.0]  # White


def midpoint_line(x0, y0, x1, y1):
    """Midpoint Line Drawing Algorithm using GL_POINTS."""
    points = []

    dx = x1 - x0
    dy = y1 - y0

    x, y = x0, y0

    x_inc = 1 if dx >= 0 else -1
    y_inc = 1 if dy >= 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx):
            points.append((x, y))
            x += x_inc
            if p >= 0:
                y += y_inc
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            points.append((x, y))
            y += y_inc
            if p >= 0:
                x += x_inc
                p += 2 * (dx - dy)
            else:
                p += 2 * dx

    return points


def draw_line(x0, y0, x1, y1):
    """Draw line using midpoint and GL_POINTS"""
    # Convert from float to integer screen coords
    scale = 1000  # arbitrary scaling to use pixel-like grid
    points = midpoint_line(int(x0 * scale), int(y0 * scale),
                           int(x1 * scale), int(y1 * scale))
    for x, y in points:
        glVertex2f(x / scale, y / scale)


def draw_catcher():
    """Draw square (catcher) with midpoint lines"""
    top_width = catcher_width
    bottom_width = catcher_width * 0.6  # narrower bottom
    half_top = top_width / 2
    half_bottom = bottom_width / 2
    half_height = catcher_height / 2

    top = catcher_y + half_height
    bottom = catcher_y - half_height

    # Top corners
    top_left = (catcher_x - half_top, top)
    top_right = (catcher_x + half_top, top)

    # Bottom corners
    bottom_left = (catcher_x - half_bottom, bottom)
    bottom_right = (catcher_x + half_bottom, bottom)

    glBegin(GL_POINTS)
    draw_line(*top_left, *top_right)         # Top
    draw_line(*top_right, *bottom_right)     # Right slope
    draw_line(*bottom_right, *bottom_left)   # Bottom
    draw_line(*bottom_left, *top_left)       # Left slope
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    glFlush()


def special_keys(key, x, y):
    global catcher_x
    if key == GLUT_KEY_LEFT:
        catcher_x -= catcher_shift
    elif key == GLUT_KEY_RIGHT:
        catcher_x += catcher_shift
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Moveable catcher with Midpoint Line")
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)

    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glColor3f(1.0, 1.0, 1.0)  # white points
    glPointSize(2.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)  # coordinate system

    glutMainLoop()


if __name__ == "__main__":
    main()
