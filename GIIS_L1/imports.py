from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from enum import Enum
from algorithmCDA import algorithmCDA
from algorithmBREZENHEM import algorithmBREZENHEM
from algorithmWU import algorithmWU
import sys
import time
import math

class Algorithm(Enum):
    CDA = 0
    BREZENHEM = 1
    WU = 2