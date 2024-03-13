from imports import *


class BaseCurveItem(QGraphicsItem):
    def __init__(self, parent=None):
        super(BaseCurveItem, self).__init__(parent)
        self.points = []

    def boundingRect(self):
        return self.childrenBoundingRect()

    def paint(self, painter, option, widget):
        steps = 100
        delta_t = 1.0 / steps
        prev_point = self.pointAtParameter(0)

        for i in range(1, steps + 1):
            t = i * delta_t
            current_point = self.pointAtParameter(t)
            line = QGraphicsLineItem(prev_point.x(), prev_point.y(), current_point.x(), current_point.y())
            line.setPen(QColor(0, 0, 255))
            line.setParentItem(self)
            prev_point = current_point

    def pointAtParameter(self, t):
        raise NotImplementedError("")


class HermiteCurveItem(BaseCurveItem):
    def __init__(self, p1, t1, p2, t2, parent=None):
        super(HermiteCurveItem, self).__init__(parent)
        self.points = [p1, t1, p2, t2]

    def pointAtParameter(self, t):
        t2 = t * t
        t3 = t2 * t
        h1 = 2 * t3 - 3 * t2 + 1
        h2 = -2 * t3 + 3 * t2
        h3 = t3 - 2 * t2 + t
        h4 = t3 - t2

        x = h1 * self.points[0].x() + h2 * self.points[2].x() + h3 * self.points[1].x() + h4 * self.points[3].x()
        y = h1 * self.points[0].y() + h2 * self.points[2].y() + h3 * self.points[1].y() + h4 * self.points[3].y()

        return QPointF(x, y)


class BezierCurveItem(BaseCurveItem):
    def __init__(self, p0, p1, p2, p3, parent=None):
        super(BezierCurveItem, self).__init__(parent)
        self.points = [p0, p1, p2, p3]

    def pointAtParameter(self, t):
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt

        x = mt3 * self.points[0].x() + 3 * mt2 * t * self.points[1].x() + 3 * mt * t2 * self.points[2].x() + t3 * \
            self.points[3].x()
        y = mt3 * self.points[0].y() + 3 * mt2 * t * self.points[1].y() + 3 * mt * t2 * self.points[2].y() + t3 * \
            self.points[3].y()

        return QPointF(x, y)


class BSplineCurveItem(BaseCurveItem):
    def __init__(self, p0, p1, p2, p3, parent=None):
        super(BSplineCurveItem, self).__init__(parent)
        self.points = [p0, p1, p2, p3]

    def pointAtParameter(self, t):
        n = len(self.points) - 1
        if n < 1:
            return QPointF(0, 0)

        t = max(0.0, min(1.0, t))
        span = int(t * n)
        span = max(0, min(n - 1, span))

        u = t * n - span
        p0, p1, p2, p3 = self.points[0], self.points[1], self.points[2], self.points[3]

        x = (1 - u) ** 3 * p0.x() + 3 * (1 - u) ** 2 * u * p1.x() + 3 * (1 - u) * u ** 2 * p2.x() + u ** 3 * p3.x()
        y = (1 - u) ** 3 * p0.y() + 3 * (1 - u) ** 2 * u * p1.y() + 3 * (1 - u) * u ** 2 * p2.y() + u ** 3 * p3.y()

        return QPointF(x, y)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.curve_item = None
        self.current_algorithm = None

    def setAlgorithm(self, algorithm):
        if algorithm == Algorithm.HERMITE:
            self.curve_item = HermiteCurveItem(QPointF(0, 0), QPointF(100, 100), QPointF(200, 0), QPointF(300, 100))
        elif algorithm == Algorithm.BEZIER:
            self.curve_item = BezierCurveItem(QPointF(0, 0), QPointF(100, 100), QPointF(200, 0), QPointF(300, 100))
        elif algorithm == Algorithm.B_SPLINE:
            self.curve_item = BSplineCurveItem(QPointF(0, 0), QPointF(100, 100), QPointF(200, 0), QPointF(300, 100))

        self.clear()
        if self.curve_item:
            self.addItem(self.curve_item)


class Paint(QWidget):
    def __init__(self):
        super(Paint, self).__init__()

        self.view = QGraphicsView()
        self.scene = GraphicsScene(self)
        self.view.setScene(self.scene)

        self.algorithm_combo = QComboBox()
        for algorithm in Algorithm:
            self.algorithm_combo.addItem(algorithm.name)
        self.algorithm_combo.currentIndexChanged.connect(self.updateAlgorithm)

        self.point_edit_labels = []
        self.point_edit_boxes = []

        for i in range(4):
            label = QLabel(f'Точка {i + 1}:')
            edit_box = QLineEdit()
            edit_box.setPlaceholderText(f'Введите координаты x, y для точки {i + 1}')
            edit_box.editingFinished.connect(self.updatePoint)

            self.point_edit_labels.append(label)
            self.point_edit_boxes.append(edit_box)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.algorithm_combo)

        for i in range(4):
            layout.addWidget(self.point_edit_labels[i])
            layout.addWidget(self.point_edit_boxes[i])


    def updateAlgorithm(self, index):
        selected_algorithm = Algorithm(index)
        self.scene.setAlgorithm(selected_algorithm)
        self.view.setScene(self.scene)

        for i in range(4):
            point = self.scene.curve_item.points[i]
            self.point_edit_boxes[i].setText(f'{point.x()}, {point.y()}')

    def updatePoint(self):
        for i in range(4):
            try:
                x, y = map(float, self.point_edit_boxes[i].text().split(','))
                self.scene.curve_item.points[i] = QPointF(x, y)
            except ValueError:
                pass
