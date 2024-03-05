from imports import *


class DebugWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DebugWindow, self).__init__(parent)
        self.initUI()
        self.algorithm = Algorithm.CDA
        self.points = QPolygon()
        self.setMouseTracking(True)
        self.current_step = 0
        self.total_steps = 0

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Отладочное окно')

        self.button = QPushButton('Draw Step', self)
        self.button.clicked.connect(self.drawStep)

    def mousePressEvent(self, e):
        self.points << e.pos()
        self.update()

    def paintEvent(self, ev):
        qp = QPainter(self)
        color = QColor(255, 0, 0)
        pen = QPen(color, 10)
        qp.setPen(pen)
        if self.points.count() == 2 and self.total_steps > 0:
            point1 = self.points[0]
            point2 = self.points[1]
            x1, y1 = point1.x(), point1.y()
            x2, y2 = point2.x(), point2.y()
            self.paintLine(x1, y1, x2, y2, qp, self.current_step)

    def paintLine(self, x1, y1, x2, y2, qp, current_step):
        if self.algorithm == Algorithm.CDA:
            algorithmCDA(x1, y1, x2, y2, qp, current_step)
        if self.algorithm == Algorithm.BREZENHEM:
            algorithmBREZENHEM(x1, y1, x2, y2, qp, current_step)
        if self.algorithm == Algorithm.WU:
            algorithmWU(x1, y1, x2, y2, qp, current_step)

    def drawStep(self):
        if self.points.count() == 2:
            point1 = self.points[0]
            point2 = self.points[1]
            x1, y1 = point1.x(), point1.y()
            x2, y2 = point2.x(), point2.y()
            dx = x2 - x1
            dy = y2 - y1
            self.total_steps = math.ceil(max(abs(dx), abs(dy)))
            if self.current_step < self.total_steps:
                self.current_step += 1
                self.update()
