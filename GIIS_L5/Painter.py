from imports import *


class PolygonEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Polygon Editor")
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.points = []
        self.current_polygon = None

        self.canvas.bind("<Button-1>", self.add_point)
        self.btn_convexity = tk.Button(self.master, text="Check Convexity", command=self.check_convexity)
        self.btn_convexity.pack(side=tk.LEFT)
        self.btn_normals = tk.Button(self.master, text="Calculate Normals", command=self.calculate_normals)
        self.btn_normals.pack(side=tk.LEFT)
        self.btn_graham = tk.Button(self.master, text="Graham's Convex Hull", command=self.graham_convex_hull)
        self.btn_graham.pack(side=tk.LEFT)
        self.btn_jarvis = tk.Button(self.master, text="Jarvis Convex Hull", command=self.jarvis_convex_hull)
        self.btn_jarvis.pack(side=tk.LEFT)
        self.btn_check_point = tk.Button(self.master, text="Check Point", command=self.check_point)
        self.btn_check_point.pack(side=tk.LEFT)
        self.entry_point = tk.Entry(self.master)
        self.entry_point.pack(side=tk.LEFT)
        self.btn_clear = tk.Button(self.master, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack(side=tk.LEFT)

        self.btn_check_intersection = tk.Button(self.master, text="Check Intersection", command=self.check_intersection)
        self.btn_check_intersection.pack(side=tk.LEFT)
        self.entry_line = tk.Entry(self.master)
        self.entry_line.pack(side=tk.LEFT)

    def check_intersection(self):
        if len(self.points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        line_str = self.entry_line.get()
        try:
            x1, y1, x2, y2 = map(float, line_str.split(","))
        except ValueError:
            tk.messagebox.showwarning("Warning", "Invalid line coordinates format. Please enter as 'x1, y1, x2, y2'.")
            return

        intersections = self.line_polygon_intersections((x1, y1), (x2, y2))
        if intersections:
            tk.messagebox.showinfo("Intersection Check", f"The line intersects the polygon at {intersections}.")
        else:
            tk.messagebox.showinfo("Intersection Check", "The line does not intersect the polygon.")

    def line_polygon_intersections(self, point1, point2):
        intersections = []
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            intersection = self.line_intersection(point1, point2, p1, p2)
            if intersection:
                intersections.append(intersection)
        return intersections

    def line_intersection(self, point1, point2, point3, point4):
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3
        x4, y4 = point4
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None 
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and \
                min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4):
            return px, py
        return None

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        if self.current_polygon:
            self.canvas.delete(self.current_polygon)
        self.current_polygon = self.canvas.create_polygon(self.points, outline="blue", fill="", width=2)

    def check_convexity(self):
        if len(self.points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        is_convex = True
        n = len(self.points)
        for i in range(n):
            dx1 = self.points[(i + 2) % n][0] - self.points[(i + 1) % n][0]
            dy1 = self.points[(i + 2) % n][1] - self.points[(i + 1) % n][1]
            dx2 = self.points[i][0] - self.points[(i + 1) % n][0]
            dy2 = self.points[i][1] - self.points[(i + 1) % n][1]
            cross_product = dx1 * dy2 - dy1 * dx2
            if cross_product < 0:
                is_convex = False
                break

        if is_convex:
            tk.messagebox.showinfo("Convexity Check", "The polygon is convex.")
        else:
            tk.messagebox.showinfo("Convexity Check", "The polygon is not convex.")

    def calculate_normals(self):
        if len(self.points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        normals = []
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            normal = ((p1[1] - p2[1]), (p2[0] - p1[0]))
            normals.append(normal)

        tk.messagebox.showinfo("Normals", f"The normals are: {normals}")

    def clear_canvas(self):
        self.points = []
        self.canvas.delete("all")

    def graham_convex_hull(self):
        points = self.points[:]
        self.clear_canvas()
        if len(points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        points = sorted(points)
        stack = []
        for point in points:
            while len(stack) >= 2 and self.orientation(stack[-2], stack[-1], point) <= 0:
                stack.pop()
            stack.append(point)

        self.canvas.create_polygon(stack, outline="red", fill="", width=2)

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    def jarvis_convex_hull(self):
        points = self.points[:]
        self.clear_canvas()
        if len(points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        hull = []
        start_point = min(points)
        current_point = start_point
        while True:
            hull.append(current_point)
            endpoint = points[0]
            for point in points:
                if (endpoint == current_point) or self.orientation(current_point, point, endpoint) == -1:
                    endpoint = point
            current_point = endpoint
            if current_point == start_point:
                break

        self.canvas.create_polygon(hull, outline="green", fill="", width=2)

    def check_point(self):
        if len(self.points) < 3:
            tk.messagebox.showwarning("Warning", "At least 3 points are needed to form a polygon.")
            return

        point_str = self.entry_point.get()
        try:
            x, y = map(float, point_str.split(","))
        except ValueError:
            tk.messagebox.showwarning("Warning", "Invalid point coordinates format. Please enter as 'x, y'.")
            return

        if self.point_in_polygon((x, y)):
            tk.messagebox.showinfo("Point Check", f"The point ({x}, {y}) is inside the polygon.")
        else:
            tk.messagebox.showinfo("Point Check", f"The point ({x}, {y}) is outside the polygon.")

    def point_in_polygon(self, point):
        x, y = point
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

