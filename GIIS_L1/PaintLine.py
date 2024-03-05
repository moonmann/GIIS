from imports import *
from DebugMenu import DebugWindow


class Paint(QMainWindow):
    def __init__(self, width=1000, height=1000, alg=Algorithm.CDA):
        super().__init__()
        self.algorithm = alg
        self.initUI(width, height)
        self.setMouseTracking(True)
        self.points = QPolygon()

    def initUI(self, width, height):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        menu_bar = self.menuBar()
        self.algorithm_menu = menu_bar.addMenu(f'Algorithm: {self.algorithm.name}')

        cda_action = QAction('CDA', self)
        cda_action.triggered.connect(lambda: self.setAlgorithm(Algorithm.CDA))
        self.algorithm_menu.addAction(cda_action)

        brezenhem_action = QAction('Bresenham', self)
        brezenhem_action.triggered.connect(lambda: self.setAlgorithm(Algorithm.BREZENHEM))
        self.algorithm_menu.addAction(brezenhem_action)

        wu_action = QAction('Wu', self)
        wu_action.triggered.connect(lambda: self.setAlgorithm(Algorithm.WU))
        self.algorithm_menu.addAction(wu_action)

        debug_action = QAction('Отладка', self)
        debug_action.triggered.connect(self.showDebugWindow)
        menu_bar.addAction(debug_action)

        self.setGeometry(200, 200, width, height)
        self.show()

    def setAlgorithm(self, alg):
        self.algorithm = alg
        self.points.clear()
        self.algorithm_menu.setTitle(f'Algorithm: {alg.name}')
        self.update()

    def showDebugWindow(self):
        debug_window = DebugWindow(self)
        debug_window.show()

    def mousePressEvent(self, e):
        self.points << e.pos()
        self.update()

    def paintEvent(self, ev):
        qp = QPainter(self)
        color = QColor(255, 0, 0)
        pen = QPen(color, 10)
        qp.setPen(pen)
        if self.points.count() % 2 == 0:
            for i in range(0, len(self.points), 2):
                point1 = self.points[i]
                point2 = self.points[i + 1]
                x1, y1 = point1.x(), point1.y()
                x2, y2 = point2.x(), point2.y()
                self.__paintLine(x1, y1, x2, y2, qp)

    def __paintLine(self, x1, y1, x2, y2, qp):
        if self.algorithm == Algorithm.CDA:
            algorithmCDA(x1, y1, x2, y2, qp, -1)
        if self.algorithm == Algorithm.BREZENHEM:
            algorithmBREZENHEM(x1, y1, x2, y2, qp, -1)
        if self.algorithm == Algorithm.WU:
            algorithmWU(x1, y1, x2, y2, qp, -1)
