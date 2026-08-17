import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter


class PixelForge:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelForge - Image Editor")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.image = None
        self.display_image = None
        self.original_image = None

        self.create_ui()

    def create_ui(self):
        # Header
        header = tk.Frame(self.root, height=80)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="PIXELFORGE",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(15, 0))

        subtitle = tk.Label(
            header,
            text="Simple Python Image Editor",
            font=("Arial", 10)
        )
        subtitle.pack()

        # Toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(pady=15)

        buttons = [
            ("Open", self.open_image),
            ("Grayscale", self.grayscale),
            ("Rotate", self.rotate),
            ("Blur", self.blur),
            ("Brightness +", self.brightness_up),
            ("Brightness -", self.brightness_down),
            ("Resize", self.resize_image),
            ("Reset", self.reset_image),
            ("Save", self.save_image),
        ]

        for text, command in buttons:
            tk.Button(
                toolbar,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                padx=8,
                pady=6
            ).pack(side="left", padx=3)

        # Image area
        self.image_frame = tk.Frame(
            self.root,
            width=900,
            height=500,
            relief="sunken",
            borderwidth=2
        )
        self.image_frame.pack(pady=10)

        self.image_label = tk.Label(
            self.image_frame,
            text="Open an image to start editing",
            font=("Arial", 14)
        )
        self.image_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Status
        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9)
        )
        self.status.pack(pady=5)

    # -------------------------
    # Open Image
    # -------------------------
    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp")
            ]
        )

        if not path:
            return

        try:
            self.image = Image.open(path).convert("RGB")
            self.original_image = self.image.copy()

            self.show_image()
            self.status.config(
                text=f"Opened: {path.split('/')[-1]}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not open image:\n{error}"
            )

    # -------------------------
    # Display Image
    # -------------------------
    def show_image(self):
        if self.image is None:
            return

        preview = self.image.copy()
        preview.thumbnail((880, 480))

        self.display_image = ImageTk.PhotoImage(preview)

        self.image_label.config(
            image=self.display_image,
            text=""
        )

    # -------------------------
    # Grayscale
    # -------------------------
    def grayscale(self):
        if not self.check_image():
            return

        self.image = self.image.convert("L").convert("RGB")

        self.show_image()
        self.status.config(text="Grayscale applied")

    # -------------------------
    # Rotate
    # -------------------------
    def rotate(self):
        if not self.check_image():
            return

        self.image = self.image.rotate(
            90,
            expand=True
        )

        self.show_image()
        self.status.config(text="Image rotated 90°")

    # -------------------------
    # Blur
    # -------------------------
    def blur(self):
        if not self.check_image():
            return

        self.image = self.image.filter(
            ImageFilter.GaussianBlur(radius=3)
        )

        self.show_image()
        self.status.config(text="Blur applied")

    # -------------------------
    # Brightness
    # -------------------------
    def brightness_up(self):
        if not self.check_image():
            return

        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1.2)

        self.show_image()
        self.status.config(text="Brightness increased")

    def brightness_down(self):
        if not self.check_image():
            return

        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(0.8)

        self.show_image()
        self.status.config(text="Brightness decreased")

    # -------------------------
    # Resize
    # -------------------------
    def resize_image(self):
        if not self.check_image():
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Resize Image")
        dialog.geometry("300x220")
        dialog.resizable(False, False)

        tk.Label(
            dialog,
            text="Width"
        ).pack(pady=(20, 5))

        width_entry = tk.Entry(dialog)
        width_entry.pack()

        tk.Label(
            dialog,
            text="Height"
        ).pack(pady=(10, 5))

        height_entry = tk.Entry(dialog)
        height_entry.pack()

        def apply_resize():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())

                if width <= 0 or height <= 0:
                    raise ValueError

                self.image = self.image.resize(
                    (width, height)
                )

                self.show_image()
                self.status.config(
                    text=f"Resized to {width} × {height}"
                )

                dialog.destroy()

            except ValueError:
                messagebox.showerror(
                    "Invalid Size",
                    "Enter valid positive numbers."
                )

        tk.Button(
            dialog,
            text="Apply",
            command=apply_resize,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=6
        ).pack(pady=20)

    # -------------------------
    # Reset
    # -------------------------
    def reset_image(self):
        if self.original_image is None:
            return

        self.image = self.original_image.copy()

        self.show_image()
        self.status.config(text="Image reset")

    # -------------------------
    # Save
    # -------------------------
    def save_image(self):
        if not self.check_image():
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("WebP Image", "*.webp")
            ]
        )

        if not path:
            return

        try:
            self.image.save(path)

            messagebox.showinfo(
                "Saved",
                "Image saved successfully!"
            )

            self.status.config(
                text="Image saved successfully"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save image:\n{error}"
            )

    # -------------------------
    # Check Image
    # -------------------------
    def check_image(self):
        if self.image is None:
            messagebox.showwarning(
                "No Image",
                "Please open an image first."
            )
            return False

        return True


# -----------------------------
# Start Application
# -----------------------------

root = tk.Tk()
app = PixelForge(root)
root.mainloop()