def algorithmBREZENHEM(x1, y1, x2, y2, qp, current_step):
    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = abs(y2 - y1)
    error = dx // 2
    ystep = 1 if y1 < y2 else -1
    y = y1

    if current_step != -1:
        for x in range(current_step):
            qp.drawPoint(y if steep else x, x if steep else y)
            error -= dy
            if error < 0:
                y += ystep
                error += dx
    else:
        for x in range(x1, x2 + 1):
            qp.drawPoint(y if steep else x, x if steep else y)
            error -= dy
            if error < 0:
                y += ystep
                error += dx
