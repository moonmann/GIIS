def algorithmCDA(x1, y1, x2, y2, qp, current_step):
    dx = x2 - x1
    dy = y2 - y1

    length = max(abs(dx), abs(dy)) if max(abs(dx), abs(dy)) != 0 else 1

    x_increment = dx / length
    y_increment = dy / length

    x = x1
    y = y1
    qp.drawPoint(x, y)

    if current_step != -1:
        for _ in range(current_step):
            x += x_increment
            y += y_increment
            qp.drawPoint(x, y)
    else:
        for _ in range(length):
            x += x_increment
            y += y_increment
            qp.drawPoint(x, y)