import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Toplevel, Label, Button
from PIL import Image, ImageTk, ImageSequence

class GIFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF Generator")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TProgressbar", thickness=20)

        self.frame = ttk.Frame(root, padding="10")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.label_title = ttk.Label(self.frame, text="GIF Generator", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=10)

        self.label1 = ttk.Label(self.frame, text="Select first image:")
        self.label1.pack(pady=5)

        self.btn_browse1 = ttk.Button(self.frame, text="Browse", command=self.browse_image1)
        self.btn_browse1.pack(pady=5)

        self.label2 = ttk.Label(self.frame, text="Select second image:")
        self.label2.pack(pady=5)

        self.btn_browse2 = ttk.Button(self.frame, text="Browse", command=self.browse_image2)
        self.btn_browse2.pack(pady=5)

        self.btn_generate = ttk.Button(self.frame, text="Generate GIF", command=self.generate_gif)
        self.btn_generate.pack(pady=20)

        self.progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=10)

        self.image1_path = ""
        self.image2_path = ""

    def browse_image1(self):
        self.image1_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.image1_path:
            self.label1.config(text=f"Selected: {self.image1_path.split('/')[-1]}")

    def browse_image2(self):
        self.image2_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.image2_path:
            self.label2.config(text=f"Selected: {self.image2_path.split('/')[-1]}")

    def generate_gif(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showerror("Error", "Please select both images")
            return

        try:
            image1 = Image.open(self.image1_path)
            image2 = Image.open(self.image2_path)
            gif_path = "temp.gif"
            self.progress.start(10)
            image1.save(gif_path, save_all=True, append_images=[image2], duration=500, loop=0)
            self.progress.stop()
            self.progress['value'] = 100

            self.show_gif(gif_path)
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"Failed to create GIF: {e}")

    def show_gif(self, gif_path):
        def save_gif():
            save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
            if save_path:
                with open(gif_path, 'rb') as original:
                    with open(save_path, 'wb') as copy:
                        copy.write(original.read())
                messagebox.showinfo("Success", f"GIF saved successfully at {save_path}")

        top = Toplevel(self.root)
        top.title("GIF Preview")
        top.geometry("300x300")
        top.configure(bg="#f0f0f0")

        frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(gif_path))]

        lbl = Label(top, bg="#f0f0f0")
        lbl.pack(expand=True)

        def update_frame(index):
            frame = frames[index]
            lbl.config(image=frame)
            index = (index + 1) % len(frames)
            top.after(100, update_frame, index)

        update_frame(0)

        btn_save = Button(top, text="Save GIF", command=save_gif, font=("Arial", 12))
        btn_save.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GIFGeneratorApp(root)
    root.mainloop()
