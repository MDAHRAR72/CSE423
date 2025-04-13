from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Size of window
w_width, w_height = 600, 800

# Catcher properties
catcher_x = 0
catcher_y = -0.96
catcher_width = 0.4
catcher_height = 0.05
catcher_shift = 0.05
catcher_color = [1.0, 1.0, 1.0]             # White

# Diamond properties
diamond_x = 0
diamond_y = 1
diamond_size = 0.08
fall_speed = 0.0004
max_fall_speed = 0.003
diamond_color = [0.0, 1.0, 1.0]             # Cyan

# Game variables
score = 0
game_over = False

# Reset button properties
reset_button_pos = (-0.85, 0.85)
reset_button_size = 0.1
reset_button_color = [1.0, 0.0, 0.0]        # Red

# Play Pause button
pause_button_pos = (0, 0.85)
pause_button_size = 0.1
pause_button_color = [0.0, 0.0, 1.0]        # Blue
pause = False

# Close button
close_button_pos = (0.85, 0.85)
close_button_size = 0.05
close_button_color = [1.0, 1.0, 0.0]        # Yellow


# Midpoint
def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6


def conv_to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def conv_from_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def draw_midpoint_zone0(x0, y0, x1, y1):
    points = []

    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = x0, y0
    while x <= x1:
        points.append((x, y))
        if d > 0:
            y += 1
            d += incNE
        else:
            d += incE
        x += 1

    return points


def midpoint(x0, y0, x1, y1):
    points = []

    zone = find_zone(x0, y0, x1, y1)
    x0_z, y0_z = conv_to_zone_0(x0, y0, zone)
    x1_z, y1_z = conv_to_zone_0(x1, y1, zone)

    if x0_z > x1_z:
        x0_z, y0_z, x1_z, y1_z = x1_z, y1_z, x0_z, y0_z

    zone_points = draw_midpoint_zone0(x0_z, y0_z, x1_z, y1_z)
    points = [conv_from_zone_0(x, y, zone) for x, y in zone_points]

    return points


def draw_line(x0, y0, x1, y1):
    scale = 1000
    points = midpoint(int(x0 * scale), int(y0 * scale),
                      int(x1 * scale), int(y1 * scale))
    for x, y in points:
        glVertex2f(x / scale, y / scale)
# Midpoint Drawing done


# Draw Catcher
def draw_catcher():
    glColor3f(*catcher_color)
    top_width = catcher_width
    bottom_width = catcher_width * 0.6
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


# Draw Diamond
def draw_diamond():
    glColor3f(*diamond_color)
    x, y = diamond_x, diamond_y
    size = diamond_size

    diamond = [
        (x, y + size + 0.03),  # top
        (x - size, y),  # left
        (x, y - size - 0.03),  # bottom
        (x + size, y),  # right
    ]

    glBegin(GL_POINTS)
    draw_line(*diamond[0], *diamond[1])  # Top to Left
    draw_line(*diamond[1], *diamond[2])  # Left to Bottom
    draw_line(*diamond[2], *diamond[3])  # Bottom to Right
    draw_line(*diamond[3], *diamond[0])  # Right to Top
    glEnd()


# Draw Reset button
def draw_reset_button():
    glColor3f(*reset_button_color)
    x, y = reset_button_pos
    size = reset_button_size

    glBegin(GL_POINTS)

    arrow = [
        (x + size * 0.5, y),            # right tip
        (x - size * 0.5, y),            # left tip
        (x, y + size * 0.5),            # top
        (x, y - size * 0.5),            # bottom
    ]

    draw_line(*arrow[0], *arrow[1])
    draw_line(*arrow[0], *arrow[2])
    draw_line(*arrow[0], *arrow[3])

    glEnd()

# Draw Pause button


def draw_pause_button():
    glColor3f(*pause_button_color)
    x, y = pause_button_pos
    size = pause_button_size

    glBegin(GL_POINTS)

    if pause:
        triangle = [
            (x + size * 0.5, y),               # right tip
            (x - size * 0.5, y + size * 0.5),  # top left
            (x - size * 0.5, y - size * 0.5)   # bottom left
        ]
        draw_line(*triangle[0], *triangle[1])
        draw_line(*triangle[1], *triangle[2])
        draw_line(*triangle[2], *triangle[0])
    else:
        line1_start = (x - size * 0.25, y + size * 0.5)  # top of left line
        line1_end = (x - size * 0.25, y - size * 0.5)  # bottom of left line

        line2_start = (x + size * 0.25, y + size * 0.5)  # top of right line
        line2_end = (x + size * 0.25, y - size * 0.5)  # bottom of right line

        draw_line(*line1_start, *line1_end)
        draw_line(*line2_start, *line2_end)

    glEnd()


# Draw close button
def draw_close_button():
    glColor3f(*close_button_color)
    x, y = close_button_pos
    s = close_button_size

    glBegin(GL_POINTS)
    draw_line(x - s, y + s, x + s, y - s)  # Left Cross
    draw_line(x - s, y - s, x + s, y + s)  # Right Cross
    glEnd()


# Diamond position updating logic
def animate():
    global diamond_y, diamond_x, fall_speed, score, game_over, pause

    if not pause:
        diamond_y -= fall_speed  # Diamond Falling

        catcher_top = catcher_y + catcher_height / 2
        catcher_left = catcher_x - catcher_width / 2
        catcher_right = catcher_x + catcher_width / 2

        diamond_bottom = diamond_y - diamond_size

        # Reset the diamond position when it reaches the bottom
        if (diamond_bottom <= catcher_top <= diamond_y + diamond_size and catcher_left <= diamond_x <= catcher_right):
            score += 1
            fall_speed = min(fall_speed + 0.0002, max_fall_speed)
            print("Score:", score)
            diamond_y = 1
            diamond_x = random.uniform(-1, 1)
        elif diamond_y - diamond_size <= -1:
            game_over = True
            pause = True
            print("Game Over...Score:", score)


# Diamond update
def update():
    global pause
    if not pause:
        animate()
    glutPostRedisplay()


# Reset function
def reset():
    global catcher_x, diamond_y, diamond_x, fall_speed, game_over, pause, score
    catcher_x = 0
    diamond_y = 1
    diamond_x = random.uniform(-1, 1)
    game_over = False
    pause = False
    score = 0
    fall_speed = 0.0004


# Pause function
def toggle_pause():
    global pause
    pause = not pause


# Catcher movement
def special_keys(key, x, y):
    global catcher_x
    if not pause and not game_over:         # Only allow movement when not paused and not game_over state
        if key == GLUT_KEY_LEFT:
            if catcher_x - catcher_width / 2 > -1:
                catcher_x -= catcher_shift
        elif key == GLUT_KEY_RIGHT:
            if catcher_x + catcher_width / 2 < 1:
                catcher_x += catcher_shift
    glutPostRedisplay()


# Mouse click functions for buttons
def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse (x, y) to OpenGL coords
        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)

        norm_x = (x / width) * 2 - 1
        norm_y = 1 - (y / height) * 2  # flip y

        # Check if inside button area
        bx, by = reset_button_pos
        s = reset_button_size
        if (bx - s <= norm_x <= bx + s) and (by - s <= norm_y <= by + s):
            reset()
            glutPostRedisplay()

        # Check if inside the pause/play button area
        bx, by = pause_button_pos
        s = pause_button_size
        if (bx - s <= norm_x <= bx + s) and (by - s <= norm_y <= by + s):
            if not game_over:  # Prevent toggling pause when game is over
                toggle_pause()
            glutPostRedisplay()

        # Check if inside the close (X) button area
        bx, by = close_button_pos
        s = close_button_size
        if (bx - s <= norm_x <= bx + s) and (by - s <= norm_y <= by + s):
            print("Game Closed...Bye")
            glutLeaveMainLoop()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    draw_diamond()
    draw_reset_button()
    draw_pause_button()
    draw_close_button()
    glFlush()


def main():
    global catcher_color, diamond_color, reset_button_color, pause_button_color, close_button_color
    catcher_color = [0.0, 1.0, 0.0]
    diamond_color = [0.0, 1.0, 1.0]
    reset_button_color = [1.0, 0.0, 0.0]
    pause_button_color = [0.0, 0.0, 1.0]
    close_button_color = [1.0, 1.0, 0.0]

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(w_width, w_height)
    glutCreateWindow(b"Catch the Diamonds!")
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse_click)

    glutIdleFunc(update)

    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)  # coordinate system

    glutMainLoop()


if __name__ == "__main__":
    main()
