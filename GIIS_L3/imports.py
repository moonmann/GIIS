from PyQt5.QtWidgets import QApplication,QSpinBox, QGraphicsItem, QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout, \
    QPushButton, QComboBox, QGraphicsLineItem, QGraphicsSceneMouseEvent, QInputDialog, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPointF
import sys
from enum import Enum

class Algorithm(Enum):
    HERMITE = 0
    BEZIER = 1
    B_SPLINE = 2