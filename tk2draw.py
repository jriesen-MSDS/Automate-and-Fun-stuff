import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Drawing App")

        # Set up canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=500, height=400, cursor="crosshair")
        self.canvas.pack()

        # Setup image to store canvas for saving
        self.image = Image.new("RGB", (500, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Variables for drawing
        self.previous_x = None
        self.previous_y = None
        self.pen_color = "black"

        # Add buttons and controls
        self.add_buttons()

    def add_buttons(self):
        # Color Picker
        self.color_button = tk.Button(self.root, text="Pick Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        # Brush Size Adjust
        self.size_label = tk.Label(self.root, text="Brush Size:")
        self.size_label.pack(side=tk.LEFT, padx=5)

        self.size_scale = tk.Scale(self.root, from_=1, to_=10, orient=tk.HORIZONTAL)
        self.size_scale.set(3)  # Default brush size
        self.size_scale.pack(side=tk.LEFT)

        # Clear Button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Save Button
        self.save_button = tk.Button(self.root, text="Save Drawing", command=self.save_drawing)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Bind mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def choose_color(self):
        # Open color picker
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def paint(self, event):
        # Draw on the canvas
        pen_size = self.size_scale.get()  # Fetch the current brush size
        if self.previous_x and self.previous_y:
            self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, width=pen_size,
                                    fill=self.pen_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([(self.previous_x, self.previous_y), (event.x, event.y)], fill=self.pen_color,
                           width=pen_size)
        self.previous_x = event.x
        self.previous_y = event.y

    def reset(self, event):
        # Reset coordinates after drawing
        self.previous_x = None
        self.previous_y = None

    def clear_canvas(self):
        # Clear the canvas and reset image
        self.canvas.delete("all")
        self.image = Image.new("RGB", (500, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_drawing(self):
        # Save the drawing as an image file
        try:
            file_path = "drawing.png"
            self.image.save(file_path)
            messagebox.showinfo("Success", f"Drawing saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving drawing: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
