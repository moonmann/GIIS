from imports import *
from ShapeClass import Point, Shape


class Paint3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Paint")

        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.axis('on')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=4)

        self.points = []
        self.shapes = []

        self.selected_shape = None

        self.preview_point = Point(x=0, y=0, z=0)

        self.point_frame = tk.Frame(self.root)
        self.point_frame.grid(row=0, column=1, padx=10, pady=10)

        self.shapes_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.shapes_listbox.grid(row=1, column=1, padx=10, pady=10)
        self.shapes_listbox.bind("<<ListboxSelect>>", self.select_shape)

        self.root.bind("<KeyPress-a>", self.move_shape_x_plus)
        self.root.bind("<KeyPress-z>", self.move_shape_x_minus)
        self.root.bind("<KeyPress-s>", self.move_shape_y_plus)
        self.root.bind("<KeyPress-x>", self.move_shape_y_minus)
        self.root.bind("<KeyPress-d>", self.move_shape_z_plus)
        self.root.bind("<KeyPress-c>", self.move_shape_z_minus)

        self.root.bind("<KeyPress-q>", self.rotate_selected_shape_x)
        self.root.bind("<KeyPress-w>", self.rotate_selected_shape_y)
        self.root.bind("<KeyPress-e>", self.rotate_selected_shape_z)

        self.root.bind("<KeyPress-r>", self.scale_selected_shape_plus_ten_percent)
        self.root.bind("<KeyPress-f>", self.scale_selected_shape_minus_ten_percent)

        self.file_menu = tk.Menu(root, tearoff=False)
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        root.config(menu=self.file_menu)

    def open_file(self):
        self.clear_all()
        try:
            with open("object.txt", "r") as file:
                for line in file:
                    num_points, *points_str = line.strip().split(" ")
                    num_points = int(num_points)
                    points = [Point(*map(float, point.split(","))) for point in points_str]
                    self.shapes.append(Shape(points))
            self.update_plot()
            self.update_shapes_listbox()
        except FileNotFoundError:
            print("Error: File not found")

    def scale_selected_shape_plus_ten_percent(self, *args):
        print('r')
        if self.selected_shape:
            self.selected_shape.scale(1.1)
            self.update_plot()

    def scale_selected_shape_minus_ten_percent(self, *args):
        if self.selected_shape:
            self.selected_shape.scale(0.9)
            self.update_plot()

    def rotate_selected_shape_x(self, *args):
        if self.selected_shape:
            self.selected_shape.rotate(np.pi / 4, 'x')
            self.update_plot()

    def rotate_selected_shape_y(self, *args):
        if self.selected_shape:
            self.selected_shape.rotate(np.pi / 4, 'y')
            self.update_plot()

    def rotate_selected_shape_z(self, *args):
        if self.selected_shape:
            self.selected_shape.rotate(np.pi / 4, 'z')
            self.update_plot()

    def move_shape_x_plus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.x += 1
            self.update_plot()

    def move_shape_x_minus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.x -= 1
            self.update_plot()

    def move_shape_y_plus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.y += 1
            self.update_plot()

    def move_shape_y_minus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.y -= 1
            self.update_plot()

    def move_shape_z_plus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.z += 1
            self.update_plot()

    def move_shape_z_minus(self, *args):
        if self.selected_shape:
            for point in self.selected_shape.points:
                point.z -= 1
            self.update_plot()

    def select_shape(self, event):
        selected_index = self.shapes_listbox.curselection()
        if selected_index:
            self.selected_shape = self.shapes[selected_index[0]]
        self.update_shapes_listbox()
        self.update_plot()

    def clear_all(self):
        self.points = []
        self.selection_points = []
        self.selected_shape = None
        self.shapes = []
        self.update_plot()
        self.update_shapes_listbox()

    def draw_shape(self, x_values, y_values, z_values):
        num_steps = 20
        if len(x_values) >= 3:
            lines = []
            for i in range(len(x_values)):
                for j in range(i + 1, len(x_values)):
                    lines.append([i, j])

            interpolated_lines = []
            for line in lines:
                x_interp = np.linspace(x_values[line[0]], x_values[line[1]], num_steps)
                y_interp = np.linspace(y_values[line[0]], y_values[line[1]], num_steps)
                z_interp = np.linspace(z_values[line[0]], z_values[line[1]], num_steps)
                interpolated_lines.append(list(zip(x_interp, y_interp, z_interp)))

            for line in interpolated_lines:
                x, y, z = zip(*line)
                self.ax.plot(x, y, z, color='black', linewidth=1)
        else:
            self.ax.plot(x_values, y_values, z_values)

    def create_shape(self):
        shape = Shape(self.points)
        self.shapes.append(shape)
        self.points = []
        self.update_plot()
        self.update_shapes_listbox()

    def update_plot(self):
        self.ax.clear()

        for shape in self.shapes:
            points = shape.points
            x_values = [point.x for point in points]
            y_values = [point.y for point in points]
            z_values = [point.z for point in points]
            self.draw_shape(x_values, y_values, z_values)

        if self.points:
            marked_x = [point.x for point in self.points]
            marked_y = [point.y for point in self.points]
            marked_z = [point.z for point in self.points]
            self.ax.scatter(marked_x, marked_y, marked_z, color='red', s=50)

        if self.preview_point:
            self.ax.scatter(self.preview_point.x, self.preview_point.y, self.preview_point.z, color='green', s=50)

        if self.selected_shape:
            self.selected_shape.update_center_point()
            for point in self.selected_shape.points:
                self.ax.scatter(point.x, point.y, point.z, color='cyan', s=50)
            self.ax.scatter(self.selected_shape.center_point.x, self.selected_shape.center_point.y,
                            self.selected_shape.center_point.z, color='purple', s=20)

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        self.canvas.draw()

    def update_shapes_listbox(self):
        self.shapes_listbox.delete(0, tk.END)
        for shape in self.shapes:
            self.shapes_listbox.insert(tk.END, f"Shape {self.shapes.index(shape) + 1}")
