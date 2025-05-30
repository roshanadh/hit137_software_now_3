import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

class ImageEditor:
    """
    This is the class for the Editor interface
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor - HIT137")

        # references used to store actual image data
        self.original_img = None
        self.cropped_img = None

        # references used to display the original and cropped images on the UI
        self.tk_img = None
        self.tk_cropped = None

        # co-ordinates for the cropping rectangle
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect_id = None

        self.build_interface()

    def build_interface(self):
        # Main frame for the canvas
        canvas_frame = tk.Frame(self.root)
        canvas_frame.grid(row=0, column=0, sticky="nsew")

        # instruction label
        label_instruction = tk.Label(canvas_frame, text="Click and drag mouse to select the image", fg="black")
        label_instruction.pack(pady=(5, 0))
        
        # Frame for controls at the bottom
        controls_frame = tk.Frame(self.root)
        controls_frame.grid(row=1, column=0, sticky="ew")
        
        self.canvas = tk.Canvas(canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # add event listeners for cropping image
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        """
        Add controls in the bottom frame: Load Button, Slider to resize, and Save button
        """
        # Control: Load Button
        btn_load = tk.Button(controls_frame, text="Load Image", command=self.load_image)
        btn_load.grid(row=0, column=0, padx=5, pady=5)

        # Control: Resizing Slider
        self.slider = ttk.Scale(controls_frame, from_=0.1, to=2.0, value=1.0, orient='horizontal', 
                               command=self.resize_image, length=200)
        self.slider.grid(row=0, column=1, padx=5, pady=5)

        # Control: Save Button
        btn_save = tk.Button(controls_frame, text="Save Image", command=self.save_image)
        btn_save.grid(row=0, column=2, padx=5, pady=5)

        # Widget to display the cropped image
        self.label_cropped = tk.Label(controls_frame)
        self.label_cropped.grid(row=0, column=3, padx=5, pady=5)

        # Label to display dimensions of the cropped image
        self.cropped_dim_label = tk.Label(self.root, text="Dimensions: N/A")
        self.cropped_dim_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def load_image(self):
        # Open file-dialog for loading the image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if not file_path:
            return
        self.original_img = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
        self.show_image(self.original_img)

    def show_image(self, img):
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
            
        img_resized = cv2.resize(img, (canvas_width, canvas_height))
        self.tk_img = ImageTk.PhotoImage(Image.fromarray(img_resized))
        self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)

    def on_mouse_press(self, event):
        if self.original_img is None:
            return
        self.start_x = event.x
        self.start_y = event.y

        # remove any existing rectangle on each mouse press
        if self.rect_id:
            self.canvas.delete(self.rect_id)

    def on_mouse_drag(self, event):
        if self.original_img is None:
            return
        
        # remove any existing rectangle on each mouse drag
        if self.rect_id:
            self.canvas.delete(self.rect_id)

        # x1(start_x) and y1(start_y) are retained throughout the drag, but 
        # x2(event.x) and y2(event.y) are updated on each drag increment
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='green')

    def on_mouse_release(self, event):
        if self.original_img is None:
            return

        self.end_x, self.end_y = event.x, event.y

        x0, y0 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x1, y1 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        
        # Get the current canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Use default dimensions if canvas hasn't been drawn yet
        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 500

        scale_x = self.original_img.shape[1] / CANVAS_WIDTH
        scale_y = self.original_img.shape[0] / CANVAS_HEIGHT

        x0 = int(x0 * scale_x)
        y0 = int(y0 * scale_y)
        x1 = int(x1 * scale_x)
        y1 = int(y1 * scale_y)

        # Ensure coordinates are within bounds
        x0 = max(0, min(x0, self.original_img.shape[1]-1))
        y0 = max(0, min(y0, self.original_img.shape[0]-1))
        x1 = max(0, min(x1, self.original_img.shape[1]-1))
        y1 = max(0, min(y1, self.original_img.shape[0]-1))

        self.cropped_img = self.original_img[y0:y1, x0:x1]
        if self.cropped_img.size > 0:  # Ensure non-empty image
            self.show_cropped_image(self.cropped_img)
            self.modified_img = self.cropped_img

    def show_cropped_image(self, img):
        if img.size == 0:
            return
        
        # get dimensions to display
        h, w = img.shape[:2]
        self.cropped_dim_label.config(text=f"Dimensions: {w} x {h}")

        img_resized = cv2.resize(img, (150, 150))
        self.tk_cropped = ImageTk.PhotoImage(Image.fromarray(img_resized))
        self.label_cropped.configure(image=self.tk_cropped)
        self.label_cropped.image = self.tk_cropped

    def resize_image(self, val):
        if not hasattr(self, 'cropped_img') or self.cropped_img is None or self.cropped_img.size == 0:
            return
        scale = float(val)
        new_w = max(1, int(self.cropped_img.shape[1] * scale))
        new_h = max(1, int(self.cropped_img.shape[0] * scale))
        resized = cv2.resize(self.cropped_img, (new_w, new_h))
        self.show_cropped_image(resized)
        self.modified_img = resized

    def save_image(self):
        if not hasattr(self, 'modified_img') or self.modified_img is None:
            messagebox.showerror("Error", "No image found. Load an image first to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not path:
            return
        cv2.imwrite(path, cv2.cvtColor(self.modified_img, cv2.COLOR_RGB2BGR))
        messagebox.showinfo("Saved", f"Image has been saved to {path}")