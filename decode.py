import cv2
import os
import base64
import time
from Crypto.Cipher import AES
from tkinter import messagebox

# Ensure folders exist
os.makedirs("decrypted", exist_ok=True)

# AES Decryption
def unpad_message(message):
    return message[:-ord(message[-1])]

def decrypt_message(encrypted, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted))
    return unpad_message(decrypted.decode())

# Generate unique file name with timestamp
def generate_filename(prefix, extension):
    timestamp = int(time.time() * 1000)
    return f"{prefix}_{timestamp}.{extension}"

# Decode message from image
def decode_text(image_path, key):
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return

    image = cv2.imread(image_path)
    binary_message = ""
    stop_sequence = "1111111111111110"

    flat_image = image.flatten()
    for i in range(len(flat_image)):
        binary_message += str(flat_image[i] & 1)
        if binary_message.endswith(stop_sequence):
            binary_message = binary_message[:-len(stop_sequence)]  # Remove stop sequence
            break

    if len(binary_message) % 8 != 0:
        messagebox.showerror("Error", "Extracted message is corrupted.")
        return

    try:
        message = "".join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        decrypted_message = decrypt_message(message, key)

        # Save decrypted message with a unique name
        output_path = os.path.join("decrypted", generate_filename("decrypted_message", "txt"))
        with open(output_path, "w") as f:
            f.write(decrypted_message)

        messagebox.showinfo("Success", f"Decrypted message saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Decryption Failed", str(e))
