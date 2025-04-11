from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window Dimensions
w_width, w_height = 800, 600

# Game states
pause = False
gameOver = False

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
diamond_speed = 60
diamond_acceleration = 5  # speed increase per second
diamond_color = [1.0, 1.0, 1.0]  # Start with white
diamond_box = {'x': 0, 'y': 0, 'width': 0, 'height': 0}

# Catcher properties
catcher_x = 0
catcher_y = -0.8
catcher_width = 0.4
catcher_height = 0.2
catcher_shift = 0.05
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


def pauseGame():
    global pause
    if pause == False:
        pause = True
    else:
        pause = False
