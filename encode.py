import cv2
import os
import base64
import time
from Crypto.Cipher import AES
from tkinter import messagebox

# Ensure folders exist
os.makedirs("encrypted", exist_ok=True)

# AES Encryption with Padding
def pad_message(message):
    pad_length = 16 - (len(message) % 16)
    return message + chr(pad_length) * pad_length

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_msg = pad_message(message)
    return base64.b64encode(cipher.encrypt(padded_msg.encode()))

# Generate unique file name with timestamp
def generate_filename(prefix, extension):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}.{extension}"

# Encode message in image
def encode_text(image_path, message, key):
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return

    encrypted_message = encrypt_message(message, key).decode()
    binary_message = ''.join(format(ord(i), '08b') for i in encrypted_message) + '1111111111111110'

    image = cv2.imread(image_path)
    h, w, _ = image.shape

    if len(binary_message) > h * w * 3:
        messagebox.showerror("Error", "Message is too long for the image.")
        return

    # Convert image to a 1D array for faster processing
    flat_image = image.flatten()
    for i in range(len(binary_message)):
        flat_image[i] = (flat_image[i] & 0xFE) | int(binary_message[i])

    # Reshape the image back
    image = flat_image.reshape(h, w, 3)

    # Save with a unique name
    output_path = os.path.join("encrypted", generate_filename("encoded_image", "png"))
    cv2.imwrite(output_path, image)

    messagebox.showinfo("Success", f"Encoded image saved at:\n{output_path}")
