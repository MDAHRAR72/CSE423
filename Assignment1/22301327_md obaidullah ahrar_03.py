from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Window dimensions
window_width, window_height = 800, 600

# Game states
PLAY = 0
PAUSE = 1
GAME_OVER = 2

# Game variables
game_state = PLAY
score = 0
last_time = 0
current_time = 0
delta_time = 0

# Diamond properties
diamond_x = 0
diamond_y = 0
diamond_size = 20
diamond_speed = 100  # pixels per second
diamond_acceleration = 5  # speed increase per second
diamond_color = [1.0, 1.0, 1.0]  # Start with white
diamond_box = {'x': 0, 'y': 0, 'width': 0, 'height': 0}

# Catcher properties
catcher_x = window_width // 2
catcher_y = window_height - 50
catcher_width = 150
catcher_height = 30
catcher_speed = 300  # pixels per second
catcher_color = [1.0, 1.0, 1.0]  # White
catcher_box = {'x': 0, 'y': 0, 'width': 0, 'height': 0}

# Button properties
button_size = 30
restart_button = {'x': 50, 'y': 30, 'size': button_size,
                  'color': [0.0, 0.8, 0.8]}  # Teal
play_pause_button = {'x': window_width // 2, 'y': 30,
                     'size': button_size, 'color': [1.0, 0.7, 0.0]}  # Amber
exit_button = {'x': window_width - 50, 'y': 30,
               'size': button_size, 'color': [1.0, 0.0, 0.0]}  # Red

# Input state
keys = {'left': False, 'right': False}

# Midpoint Line Algorithm


def draw_line_midpoint(x1, y1, x2, y2, r, g, b):
    # Find zone
    zone = find_zone(x1, y1, x2, y2)

    # Convert to zone 0
    x1_0, y1_0 = convert_to_zone0(x1, y1, zone)
    x2_0, y2_0 = convert_to_zone0(x2, y2, zone)

    # Make sure x1_0 <= x2_0
    if x1_0 > x2_0:
        x1_0, x2_0 = x2_0, x1_0
        y1_0, y2_0 = y2_0, y1_0

    # Draw line in zone 0
    points = midpoint_line_zone0(x1_0, y1_0, x2_0, y2_0)

    # Convert back and draw points
    glColor3f(r, g, b)
    glBegin(GL_POINTS)
    for x, y in points:
        org_x, org_y = convert_from_zone0(x, y, zone)
        glVertex2f(org_x, org_y)
    glEnd()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        if dx < 0 and dy >= 0:
            return 3
        if dx < 0 and dy < 0:
            return 4
        return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        if dx < 0 and dy >= 0:
            return 2
        if dx < 0 and dy < 0:
            return 5
        return 6


def convert_to_zone0(x, y, zone):
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
    return 0, 0


def convert_from_zone0(x, y, zone):
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
    return 0, 0


def midpoint_line_zone0(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy - dx)
    x = x1
    y = y1
    points.append((x, y))

    while x < x2:
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1
        points.append((x, y))

    return points

# Shape drawing functions


def draw_diamond(x, y, size, r, g, b):
    # Draw a diamond shape using midpoint line algorithm
    draw_line_midpoint(x, y - size, x + size, y, r, g, b)  # Bottom right
    draw_line_midpoint(x + size, y, x, y + size, r, g, b)  # Top right
    draw_line_midpoint(x, y + size, x - size, y, r, g, b)  # Top left
    draw_line_midpoint(x - size, y, x, y - size, r, g, b)  # Bottom left

    # Update bounding box
    diamond_box['x'] = x - size
    diamond_box['y'] = y - size
    diamond_box['width'] = size * 2
    diamond_box['height'] = size * 2


def draw_catcher(x, y, width, height, r, g, b):
    # Draw a catcher shape using midpoint line algorithm
    half_width = width // 2
    draw_line_midpoint(x - half_width, y, x, y -
                       height, r, g, b)  # Bottom left
    draw_line_midpoint(x, y - height, x + half_width,
                       y, r, g, b)  # Bottom right
    draw_line_midpoint(x + half_width, y, x + half_width -
                       10, y + 10, r, g, b)  # Top right
    draw_line_midpoint(x + half_width - 10, y + 10, x -
                       half_width + 10, y + 10, r, g, b)  # Top
    draw_line_midpoint(x - half_width + 10, y + 10, x -
                       half_width, y, r, g, b)  # Top left

    # Update bounding box
    catcher_box['x'] = x - half_width
    catcher_box['y'] = y - height
    catcher_box['width'] = width
    catcher_box['height'] = height + 10


def draw_restart_button(x, y, size, r, g, b):
    # Draw a left arrow button
    draw_line_midpoint(x + size//2, y - size//2, x - size//2, y, r, g, b)
    draw_line_midpoint(x - size//2, y, x + size//2, y + size//2, r, g, b)
    draw_line_midpoint(x - size//4, y - size//4, x -
                       size//4, y + size//4, r, g, b)


def draw_play_button(x, y, size, r, g, b):
    # Draw a play button (triangle)
    draw_line_midpoint(x - size//3, y - size//3, x -
                       size//3, y + size//3, r, g, b)
    draw_line_midpoint(x - size//3, y - size//3, x + size//3, y, r, g, b)
    draw_line_midpoint(x - size//3, y + size//3, x + size//3, y, r, g, b)


def draw_pause_button(x, y, size, r, g, b):
    # Draw a pause button (two vertical lines)
    draw_line_midpoint(x - size//3, y - size//3, x -
                       size//3, y + size//3, r, g, b)
    draw_line_midpoint(x + size//3, y - size//3, x +
                       size//3, y + size//3, r, g, b)


def draw_exit_button(x, y, size, r, g, b):
    # Draw an X (cross) button
    draw_line_midpoint(x - size//2, y - size//2, x +
                       size//2, y + size//2, r, g, b)
    draw_line_midpoint(x - size//2, y + size//2, x +
                       size//2, y - size//2, r, g, b)

# Game logic functions


def check_collision():
    return (catcher_box['x'] < diamond_box['x'] + diamond_box['width'] and
            catcher_box['x'] + catcher_box['width'] > diamond_box['x'] and
            catcher_box['y'] < diamond_box['y'] + diamond_box['height'] and
            catcher_box['y'] + catcher_box['height'] > diamond_box['y'])


def spawn_new_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(diamond_size, window_width - diamond_size)
    diamond_y = 0  # Start at the top
    diamond_color = [random.random(), random.random(), random.random()]
    # Make sure the color is bright enough
    while sum(diamond_color) < 1.5:
        diamond_color = [random.random(), random.random(), random.random()]


def reset_game():
    global game_state, score, diamond_speed
    game_state = PLAY
    score = 0
    diamond_speed = 100
    spawn_new_diamond()
    print("Starting Over")

# OpenGL callbacks


def display():
    global diamond_y, game_state, score

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw diamond
    if game_state != GAME_OVER:
        draw_diamond(diamond_x, diamond_y, diamond_size,
                     diamond_color[0], diamond_color[1], diamond_color[2])

    # Draw catcher
    if game_state == GAME_OVER:
        draw_catcher(catcher_x, catcher_y, catcher_width,
                     catcher_height, 1.0, 0.0, 0.0)  # Red when game over
    else:
        draw_catcher(catcher_x, catcher_y, catcher_width, catcher_height,
                     catcher_color[0], catcher_color[1], catcher_color[2])

    # Draw buttons
    draw_restart_button(restart_button['x'], restart_button['y'], restart_button['size'],
                        restart_button['color'][0], restart_button['color'][1], restart_button['color'][2])

    if game_state == PAUSE:
        draw_play_button(play_pause_button['x'], play_pause_button['y'], play_pause_button['size'],
                         play_pause_button['color'][0], play_pause_button['color'][1], play_pause_button['color'][2])
    else:
        draw_pause_button(play_pause_button['x'], play_pause_button['y'], play_pause_button['size'],
                          play_pause_button['color'][0], play_pause_button['color'][1], play_pause_button['color'][2])

    draw_exit_button(exit_button['x'], exit_button['y'], exit_button['size'],
                     exit_button['color'][0], exit_button['color'][1], exit_button['color'][2])

    glutSwapBuffers()


def update(value):
    global diamond_y, game_state, score, diamond_speed, catcher_x
    global last_time, current_time, delta_time

    # Calculate delta time
    current_time = time.time()
    if last_time == 0:
        last_time = current_time
    delta_time = current_time - last_time
    last_time = current_time

    # Update game state
    if game_state == PLAY:
        # Move diamond
        diamond_y += diamond_speed * delta_time

        # Check if diamond is caught
        if check_collision():
            score += 1
            print(f"Score: {score}")
            spawn_new_diamond()
            diamond_speed += diamond_acceleration  # Increase speed

        # Check if diamond is missed
        if diamond_y > window_height:
            game_state = GAME_OVER
            print(f"Game Over! Final Score: {score}")

        # Move catcher based on key presses
        if keys['left'] and catcher_x > catcher_width // 2:
            catcher_x -= catcher_speed * delta_time
        if keys['right'] and catcher_x < window_width - catcher_width // 2:
            catcher_x += catcher_speed * delta_time

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # ~60 FPS


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC key
        glutLeaveMainLoop()

    if key == b' ':  # Space key to toggle pause
        global game_state
        if game_state == PLAY:
            game_state = PAUSE
        elif game_state == PAUSE:
            game_state = PLAY


def keyboard_special(key, x, y):
    if game_state != PLAY:
        return

    if key == GLUT_KEY_LEFT:
        keys['left'] = True
    elif key == GLUT_KEY_RIGHT:
        keys['right'] = True


def keyboard_special_up(key, x, y):
    if key == GLUT_KEY_LEFT:
        keys['left'] = False
    elif key == GLUT_KEY_RIGHT:
        keys['right'] = False


def mouse(button, state, x, y):
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return

    # Check if restart button clicked
    if (x >= restart_button['x'] - restart_button['size'] and
        x <= restart_button['x'] + restart_button['size'] and
        y >= window_height - restart_button['y'] - restart_button['size'] and
            y <= window_height - restart_button['y'] + restart_button['size']):
        reset_game()

    # Check if play/pause button clicked
    elif (x >= play_pause_button['x'] - play_pause_button['size'] and
          x <= play_pause_button['x'] + play_pause_button['size'] and
          y >= window_height - play_pause_button['y'] - play_pause_button['size'] and
          y <= window_height - play_pause_button['y'] + play_pause_button['size']):
        global game_state
        if game_state == PLAY:
            game_state = PAUSE
            print("Game Paused")
        elif game_state == PAUSE:
            game_state = PLAY
            print("Game Resumed")

    # Check if exit button clicked
    elif (x >= exit_button['x'] - exit_button['size'] and
          x <= exit_button['x'] + exit_button['size'] and
          y >= window_height - exit_button['y'] - exit_button['size'] and
          y <= window_height - exit_button['y'] + exit_button['size']):
        print(f"Goodbye! Final Score: {score}")
        glutLeaveMainLoop()


def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Catch the Diamonds!")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard_special)
    glutSpecialUpFunc(keyboard_special_up)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)

    glClearColor(0.0, 0.0, 0.1, 1.0)  # Dark blue background

    # Initialize the game
    reset_game()

    glutMainLoop()


if __name__ == "__main__":
    main()
