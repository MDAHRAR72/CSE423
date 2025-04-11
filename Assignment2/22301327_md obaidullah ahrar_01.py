from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window Dimensions
w_width, w_height = 800, 600

# Game States
play = 0
pause = 1
game_over = 2
