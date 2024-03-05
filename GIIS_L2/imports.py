from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from enum import Enum
import sys
import numpy as np
import math
import time


class Line(Enum):
    CIRCLE = 0
    ELLIPSE = 1
    HYPERBOLA = 2
    PARABOLA = 3
