import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from encode import encode_text
from decode import decode_text

def open_file(label):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if file_path:
        load_image_preview(file_path, label)
    return file_path

def load_image_preview(path, label):
    image = Image.open(path)
    image = image.resize((250, 250))
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img  # Store reference

def encryption_gui():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("Encrypt Message in Image")
    root.geometry("600x500")
    root.configure(bg="#2C2F33")

    ttk.Label(root, text="Select an Image:").pack()
    image_label = ttk.Label(root)
    image_label.pack()

    file_path_var = tk.StringVar()

    def select_file():
        file_path_var.set(open_file(image_label))

    ttk.Button(root, text="Browse", command=select_file).pack()

    ttk.Label(root, text="Enter Message:").pack()
    text_entry = ttk.Entry(root, width=50)
    text_entry.pack()

    ttk.Label(root, text="Enter Key (16 chars max):").pack()
    key_entry = ttk.Entry(root, width=50, show='*')
    key_entry.pack()

    def encode_now():
        file_path = file_path_var.get()
        message = text_entry.get()
        key = key_entry.get().ljust(16).encode()
        encode_text(file_path, message, key)

    ttk.Button(root, text="Encrypt and Save", command=encode_now).pack(pady=10)
    ttk.Button(root, text="Back", command=main_gui).pack(pady=10)

    root.mainloop()

def decryption_gui():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("Decrypt Hidden Message")
    root.geometry("600x500")
    root.configure(bg="#2C2F33")

    ttk.Label(root, text="Select Encrypted Image:").pack()
    image_label = ttk.Label(root)
    image_label.pack()

    file_path_var = tk.StringVar()

    def select_file():
        file_path_var.set(open_file(image_label))

    ttk.Button(root, text="Browse", command=select_file).pack()

    ttk.Label(root, text="Enter Key:").pack()
    key_entry = ttk.Entry(root, width=50, show='*')
    key_entry.pack()

    def decode_now():
        file_path = file_path_var.get()
        key = key_entry.get().ljust(16).encode()
        decode_text(file_path, key)

    ttk.Button(root, text="Decrypt and Save", command=decode_now).pack(pady=10)
    ttk.Button(root, text="Back", command=main_gui).pack(pady=10)

    root.mainloop()

def main_gui():
    global root
    root = tk.Tk()
    root.title("Image Steganography")
    root.geometry("400x300")
    root.configure(bg="#2C2F33")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12), background="#2C2F33", foreground="white")
    style.configure("TButton", font=("Arial", 12), padding=5)

    ttk.Label(root, text="Choose an Option:").pack(pady=20)
    ttk.Button(root, text="Encrypt Message in Image", command=encryption_gui).pack(pady=10)
    ttk.Button(root, text="Decrypt Message from Image", command=decryption_gui).pack(pady=10)

    root.mainloop()

main_gui()
