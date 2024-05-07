from imports import *


class PolygonEditor:
    def __init__(self, master, width=800, height=600):
        self.master = master
        self.master.title("Простой графический редактор")

        self.canvas = tk.Canvas(self.master, width=width, height=height, bg="#FFFFFF")
        self.canvas.pack()

        self.points = []
        self.edges = []
        self.fill_algorithm = None

        self.canvas.bind("<Button-1>", self.add_point)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.fill_menu = tk.Menu(self.menu, tearoff=0)
        self.fill_menu.add_command(label="Растровая развертка с упорядоченным списком ребер", command=self.set_fill_algorithm_edge)
        self.fill_menu.add_command(label="Простой алгоритм заполнения с затравкой", command=self.set_fill_algorithm_edge)
        self.fill_menu.add_command(label="Построчный алгоритм заполнения с затравкой", command=self.set_fill_algorithm_scanline)

        self.menu.add_cascade(label="Алгоритм заполнения", menu=self.fill_menu)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        if len(self.points) > 1:
            self.canvas.create_line(self.points[-2], self.points[-1], fill="#000000")
        if len(self.points) > 2:
            self.canvas.create_line(self.points[-1], self.points[0], fill="#000000")
        if len(self.points) > 2 and self.fill_algorithm:
            self.fill_algorithm()

    def set_fill_algorithm_edge(self):
        self.fill_algorithm = self.fill_polygon_edge

    def set_fill_algorithm_seed(self):
        self.fill_algorithm = self.fill_polygon_seed

    def set_fill_algorithm_scanline(self):
        self.fill_algorithm = self.fill_polygon_scanline

    def fill_polygon_edge(self):
        self.edges = []
        for i in range(len(self.points) - 1):
            self.edges.append((self.points[i], self.points[i + 1]))
        self.edges.append((self.points[-1], self.points[0]))

        y_list = []
        for edge in self.edges:
            y_list.append(edge[0][1])
            y_list.append(edge[1][1])
        y_list = list(set(y_list))
        y_list.sort()

        active_edges = []
        for y in range(y_list[0], y_list[-1] + 1):
            for edge in self.edges:
                if edge[0][1] <= y < edge[1][1] or edge[1][1] <= y < edge[0][1]:
                    x_intersection = int(edge[0][0] + (y - edge[0][1]) * (edge[1][0] - edge[0][0]) / (edge[1][1] - edge[0][1]))
                    active_edges.append(x_intersection)
            active_edges.sort()
            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):
                    self.canvas.create_line(active_edges[i], y, active_edges[i + 1], y, fill="#000000")
            active_edges = []

    def fill_polygon_seed(self):
        seed = self.points[0]
        stack = [seed]
        filled_points = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in filled_points:
                continue
            self.canvas.create_line(x, y, x, y, fill="#000000")
            filled_points.add((x, y))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in self.points:
                    continue
                stack.append((nx, ny))

    def fill_polygon_seed(self):
        seed = self.points[0]
        stack = [seed]
        filled_points = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in filled_points:
                continue
            self.canvas.create_line(x, y, x, y, fill="#000000")
            filled_points.add((x, y))  # Mark point as filled
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in self.points:
                    continue
                stack.append((nx, ny))

    def fill_polygon_scanline(self):
        min_y = min(y for x, y in self.points)
        max_y = max(y for x, y in self.points)

        edges = []
        for i in range(len(self.points) - 1):
            edges.append(((self.points[i][0], self.points[i][1]), (self.points[i + 1][0], self.points[i + 1][1])))
        edges.append(((self.points[-1][0], self.points[-1][1]), (self.points[0][0], self.points[0][1])))

        active_edges = []
        for y in range(min_y, max_y + 1):
            for edge in edges:
                p1, p2 = edge
                if p1[1] > p2[1]:
                    p1, p2 = p2, p1
                if p1[1] <= y < p2[1]:
                    x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    active_edges.append(x_intersect)
            active_edges.sort()
            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):
                    x1 = int(active_edges[i])
                    x2 = int(active_edges[i + 1])
                    self.canvas.create_line(x1, y, x2, y, fill="#000000")
            active_edges = []