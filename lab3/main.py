import turtle
import time
from turtle import RawTurtle, TurtleScreen
from tkinter import *


class Window(Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.running = True
        self.geometry(geometry)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.turtle = RawTurtle(TurtleScreen(self.canvas))

    def update_window(self):
        if self.running:
            self.update()

    def destroy_window(self):
        self.running = False
        self.destroy()


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
    draw_rect(t, recount_coord(x), recount_coord(y), max(cell_size, 1), max(cell_size, 1), color)


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
    # coord *= max(cell_size, 1)
    coord *= cell_size
    coord += x_start
    # print(coord)
    return round(coord)


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
    # create windows
    win1 = Window('Turtle Window 1', '800x480+0+0')
    turtle.tracer(0, 0)
    t = turtle.Turtle()
    t2 = win1.turtle
    t.shapesize(1, 1, 1)
    width = 750
    x_start = -width // 2
    y_start = x_start

    cell_size = width / max_coord
    cells_number = round(max_coord)
    multiplier = (cells_number + 99) // 100
    print(cell_size)
    # Отрисовка сетки
    draw_grid(t, x_start, y_start, cell_size * multiplier, cells_number // multiplier)

    result_string = ''

    result_string += "Масштаб: " + str(multiplier) + " точек в одной клетке\n"
    result_string += "Пошаговый алгоритм -- синяя линия\n"
    result_string += "Алгоритм Брезенхема -- зеленая линия\n"

    start_time = time.time()
    # Здесь вызывается пошаговый алгоритм
    points_simple = simple_algorithm(x1_simple, y1_simple, x2_simple, y2_simple)
    end_time = time.time()
    execution_time = end_time - start_time
    result_string += "Время рассчета пошагового алгоритма: " + str(execution_time) + '\n'

    start_time = time.time()
    # Здесь вызывается алгоритм Брезенхема
    points_bresenham = bresenham_algorithm(x1_br, y1_br, x2_br, y2_br)
    end_time = time.time()
    execution_time = end_time - start_time
    result_string += "Время рассчета алгоритма Брезенхема: " + str(execution_time) + '\n'

    t2.up()
    t2.goto(-100, -100)
    t2.down()
    t2.write(result_string, font=("Arial", 16, "normal"))

    # Отрисовка линий
    draw_points(points_simple, 'blue')
    draw_points(points_bresenham, 'green')
    # print(points_bresenham)

    turtle.update()
    turtle.mainloop()
