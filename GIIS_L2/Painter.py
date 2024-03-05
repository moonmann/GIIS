from imports import *


class Paint(QMainWindow):
    def __init__(self):
        super().__init__()

        self.point1 = None
        self.point2 = None

        self.debug_mode = True

        self.debug_button = False

        self.line_form = Line.CIRCLE

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Drawer')

        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu(self.line_form.name)
        self.file_menu.setTitle(self.line_form.name)

        circleAction = QAction('Draw Circle', self)
        circleAction.triggered.connect(self.drawCircle)

        hyperbolaAction = QAction('Draw Hyperbola', self)
        hyperbolaAction.triggered.connect(self.drawHyperbola)

        ellipseAction = QAction('Draw Ellipse', self)
        ellipseAction.triggered.connect(self.drawEllipse)

        parabolaAction = QAction('Draw Parabola', self)
        parabolaAction.triggered.connect(self.drawParabola)

        self.file_menu.addAction(circleAction)
        self.file_menu.addAction(ellipseAction)
        self.file_menu.addAction(hyperbolaAction)
        self.file_menu.addAction(parabolaAction)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.mouse_position_label = QLabel('Mouse Position:')
        statusbar.addWidget(self.mouse_position_label)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        layout.addWidget(self)
        self.show()

    def paintEvent(self, event):
        if self.point1 is not None and self.point2 is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            pen = QPen(Qt.black, 2, Qt.SolidLine)
            painter.setPen(pen)

            if self.line_form == Line.CIRCLE:
                radius = int(
                    ((self.point2.x() - self.point1.x()) ** 2 + (self.point2.y() - self.point1.y()) ** 2) ** 0.5)

                self.__drawCircle(painter, self.point1.x(), self.point1.y(), radius)

            elif self.line_form == Line.ELLIPSE:
                self.__drawEllipse(painter, self.point1, self.point2)

            elif self.line_form == Line.HYPERBOLA:
                self.__drawHyperbola(painter, self.point1, self.point2)

            elif self.line_form == Line.PARABOLA:
                self.__drawParabola(painter, self.point1, self.point2)

            self.point1 = None
            self.point2 = None

    def mousePressEvent(self, event):
        if not self.point1:
            self.point1 = event.pos()
        elif not self.point2:
            self.point2 = event.pos()
            self.update()

        self.mouse_position_label.setText(f'Mouse Position: {event.pos().x()}, {event.pos().y()}')

    def showContextMenu(self, pos):
        self.context_menu.exec_(self.mapToGlobal(pos))

    def drawCircle(self):
        self.line_form = Line.CIRCLE
        self.file_menu.setTitle(self.line_form.name)
        self.update()

    def drawEllipse(self):
        self.line_form = Line.ELLIPSE
        self.file_menu.setTitle(self.line_form.name)
        self.update()

    def drawHyperbola(self):
        self.line_form = Line.HYPERBOLA
        self.file_menu.setTitle(self.line_form.name)
        self.update()

    def drawParabola(self):
        self.line_form = Line.PARABOLA
        self.file_menu.setTitle(self.line_form.name)
        self.update()

    def __drawCircle(self, painter, center_x, center_y, radius):
        x = 0
        y = radius

        limit = 0

        error = 2 - 2 * radius

        painter.drawPoint(center_x + x, center_y + y)

        while y > limit:
            if error > 0:
                diff_1 = 2 * error - 2 * x - 1
                if diff_1 > 0:
                    y = y - 1
                    error = error - 2 * y + 1
                else:
                    x = x + 1
                    y = y - 1
                    error = error + 2 * x - 2 * y + 2
            elif error < 0:
                diff_2 = 2 * error + 2 * y - 1
                if diff_2 <= 0:
                    x = x + 1
                    error = error + 2 * x + 1
                else:
                    x = x + 1
                    y = y - 1
                    error = error + 2 * x - 2 * y + 2
            else:
                x = x + 1
                y = y - 1
                error = error + 2 * x - 2 * y + 2
            self.__plotPoints(painter, center_x, center_y, x, y)

    def __drawEllipse(self, painter, point_1, point_2):
        center_x = (point_1.x() + point_2.x()) // 2
        center_y = (point_1.y() + point_2.y()) // 2

        a = abs(point_1.x() - point_2.x()) // 2
        b = abs(point_1.y() - point_2.y()) // 2

        a_squared = a * a
        b_squared = b * b

        error = a_squared + b_squared - 2 * a_squared * b

        x = 0
        y = b

        limit = 0

        while y > limit:

            self.__plotPoints(painter, center_x, center_y, x, y)

            if error < 0:
                diff = 2*(error + a_squared*y) - 1
                if diff <= 0:
                    x = x + 1
                    error = error + b_squared*(2*x + 1)
                else:
                    x = x + 1
                    y = y - 1
                    error = error + b_squared * (2 * x + 1) + a_squared*(1 - 2*y)
            elif error > 0:
                diff = 2 * (error - b_squared * x) - 1
                if diff > 0:
                    y = y - 1
                    error = error + a_squared*(1 - 2*y)
                else:
                    x = x + 1
                    y = y - 1
                    error = error + b_squared * (2 * x + 1) + a_squared*(1 - 2*y)
            else:
                x = x + 1
                y = y - 1
                error = error + b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)

    def __drawHyperbola(self, painter, point_1, point_2):
        maj_axis = math.sqrt(pow((point_2.x() - point_1.x()), 2) + pow((point_2.y() - point_1.y()), 2))
        min_axis = maj_axis / 2

        x1, y1 = point_1.x(), point_1.y()

        maj_axis_squared = maj_axis * maj_axis
        min_axis_squared = min_axis * min_axis

        x, y = maj_axis, 0
        d = 2 * maj_axis_squared - 2 * maj_axis * min_axis_squared - min_axis_squared

        while y <= (min_axis_squared * x) / maj_axis_squared:
            self.__printPixelForHyperbola(painter, x1, y1, x, y)
            if d < 0:
                d += 2 * maj_axis_squared * (2 * y + 3)
            else:
                d += 2 * maj_axis_squared * (2 * y + 3) - 4 * min_axis_squared * (x + 1)
                x += 1
            y += 1

        init = 100
        while init > 0:
            if d < 0:
                d += 2 * min_axis_squared * (3 + 2 * x)
            else:
                d += 2 * min_axis_squared * (3 + 2 * x) - 4 * maj_axis_squared * (y + 1)
                y += 1
            x += 1
            self.__printPixelForHyperbola(painter, x1, y1, x, y)
            init -= 1

    def __drawParabola(self, painter, point_1, point_2):
        center_x = (point_1.x() + point_2.x()) / 2
        center_y = max(point_1.y(), point_2.y())

        direction = 1 if point_1.y() - point_2.y() > 0 else 0

        a = abs(point_2.x() - point_1.x()) / 2

        d = 4 - 8 * a
        x = 0
        y = 0

        while y <= 2 * a:
            self.__printPixelForParabola(painter, center_x, center_y, x, y, direction)
            if d < 0:
                d += 2 * (6 + 4 * y)
            else:
                d += 2 * (6 + 4 * y - 4 * a)
                x += 1
            y += 1

        d = 1 - 8 * a

        while x <= 2 * a:
            self.__printPixelForParabola(painter, center_x, center_y, x, y, direction)
            if d > 0:
                d += -16 * a
            else:
                d += 4 * (2 + 2 * y - 4 * a)
                y += 1
            x += 1

    def __printPixelForParabola(self, painter, x1, y1, y, x, direction):
        if direction:
            painter.drawPoint(x1 + x, y1 + y)
            painter.drawPoint(x1 - x, y1 + y)
        else:
            painter.drawPoint(x1 + x, y1 - y)
            painter.drawPoint(x1 - x, y1 - y)

    def __printPixelForHyperbola(self, painter, x1, y1, y, x):
        painter.drawPoint(x1 + x, y1 + y)
        painter.drawPoint(x1 + x, y1 - y)
        painter.drawPoint(x1 - x, y1 - y)
        painter.drawPoint(x1 - x, y1 + y)

    def __plotPoints(self, painter, center_x, center_y, x, y):
        painter.drawPoint(center_x + x, center_y + y)
        painter.drawPoint(center_x - x, center_y + y)
        painter.drawPoint(center_x + x, center_y - y)
        painter.drawPoint(center_x - x, center_y - y)
