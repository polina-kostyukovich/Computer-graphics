import turtle
import time


def draw_line(t, x1, y1, x2, y2):
    t.up()
    t.goto(x1, y1)
    t.down()
    t.goto(x2, y2)


def draw_rect(t, x, y, width, height, color):
    t.up()
    t.goto(x, y)
    t.down()
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    t.fd(width)
    t.lt(90)
    t.fd(height)
    t.lt(90)
    t.fd(width)
    t.lt(90)
    t.fd(height)
    t.lt(90)
    t.end_fill()
    t.fillcolor('black')
    t.pencolor('black')


def draw_grid(t, x_start, y_start, cell_size, cells_number):
    x_max = x_start + cell_size * cells_number
    y_max = x_max
    for i in range(cells_number):
        x = x_start + i * cell_size
        draw_line(t, x, y_start, x, y_max)
    for i in range(cells_number):
        y = y_start + i * cell_size
        draw_line(t, x_start, y, x_max, y)


def draw_pixel(t, x, y, color):
    draw_rect(t, recount_coord(x), recount_coord(y), cell_size, cell_size, color)


def simple_algorithm(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))

    if dx == 0 and dy == 0:
        return [(x1, y1)]

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    for _ in range(steps):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    return points


def bresenham_algorithm(x1, y1, x2, y2):
    points = []
    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = abs(y2 - y1)
    error = dx
    ystep = 1 if y1 < y2 else -1
    y = y1

    for x in range(x1, x2 + 1):
        points.append((y, x)) if steep else points.append((x, y))
        error -= 2 * dy
        if error < 0:
            y += ystep
            error += 2 * dx
    return points


def recount_coord(coord):
    coord *= cell_size
    coord += x_start
    return coord


def draw_points(points, color):
    for point in points:
        draw_pixel(t, point[0], point[1], color)


if __name__ == "__main__":
    x1_simple, y1_simple, x2_simple, y2_simple = map(int, input("Введите x1, y1, x2, y2 для пошагового алгоритма\n").strip().split())
    x1_br, y1_br, x2_br, y2_br = map(int, input("Введите x1, y1, x2, y2 для алгоритма Брезенхема\n").strip().split())

    x_max = max(x1_simple, x2_simple, x1_br, x2_br) * 1.05
    y_max = max(y1_simple, y2_simple, y1_br, y2_br) * 1.05
    max_coord = max(x_max, y_max) + 1

    screen = turtle.getscreen()
    t = turtle.Turtle()
    t.speed('fastest')
    # t.speed(0)
    t.shapesize(1, 1, 1)
    width = 750
    x_start = -width // 2
    y_start = x_start

    cell_size = width / max_coord
    cells_number = round(max_coord)
    multiplier = (cells_number + 99) // 100
    print("Масштаб:", multiplier, "точек в одной клетке")
    print("Пошаговый алгоритм -- синяя линия")
    print("Алгоритм Брезенхема -- зеленая линия")
    # Отрисовка сетки
    draw_grid(t, x_start, y_start, cell_size * multiplier, cells_number // multiplier)

    start_time = time.time()
    # Здесь вызывается пошаговый алгоритм
    points_simple = simple_algorithm(x1_simple, y1_simple, x2_simple, y2_simple)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Время работы пошагового алгоритма: ", execution_time)

    start_time = time.time()
    # Здесь вызывается алгоритм Брезенхема
    points_bresenham = bresenham_algorithm(x1_br, y1_br, x2_br, y2_br)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Время работы алгоритма Брезенхема: ", execution_time)

    # Отрисовка линий
    draw_points(points_simple, 'blue')
    draw_points(points_bresenham, 'green')

    turtle.mainloop()
