from PyQt5.QtGui import *


def fractional_part(value):
    return value - int(value)


def algorithmWU(x1, y1, x2, y2, qp, current_step):
    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    gradient = dy / dx if dx != 0 else 1

    error = dx // 2
    ystep = 1 if y1 < y2 else -1
    y = y1

    x_end = round(x1)
    y_end = y1 + gradient * (x_end - x1)
    x_gap = 1 - fractional_part(x1 + 0.5)

    x_pixel_end = int(x_end)
    y_pixel_end = int(y_end)
    drawPointToWU(y_pixel_end if steep else x_pixel_end, x_pixel_end if steep else y_pixel_end,
                  1 - fractional_part(y_end) * x_gap, qp)
    drawPointToWU(y_pixel_end + 1 if steep else x_pixel_end + 1, x_pixel_end if steep else y_pixel_end,
                  fractional_part(y_end) * x_gap, qp)

    inter_y = y_end + gradient

    if current_step != -1:
        for x in range(current_step):
            drawPointToWU(int(inter_y) if steep else x, x if steep else int(inter_y),
                          1 - fractional_part(inter_y), qp)
            drawPointToWU(int(inter_y) + 1 if steep else x + 1, x if steep else int(inter_y),
                          fractional_part(inter_y), qp)
            error -= dy
            inter_y += gradient
            if error < 0:
                y += ystep
                error += dx
    else:
        for x in range(x1, x2 + 1):
            drawPointToWU(int(inter_y) if steep else x, x if steep else int(inter_y),
                          1 - fractional_part(inter_y), qp)
            drawPointToWU(int(inter_y) + 1 if steep else x + 1, x if steep else int(inter_y),
                          fractional_part(inter_y), qp)
            error -= dy
            inter_y += gradient
            if error < 0:
                y += ystep
                error += dx


def drawPointToWU(x, y, intensity, qp):
    color = QColor(255, 0, 0)
    color.setAlphaF(intensity)
    pen = QPen(color, 10)
    qp.setPen(pen)
    qp.drawPoint(x, y)
