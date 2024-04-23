import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from models import CompressedImage  # Assuming you have a module named 'compress_image' for image compression

def compress_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            compressor = CompressedImage(file_path, quality=0.6)
            compressed_image = compressor.CompressedImage()
            img = Image.open(compressed_image)
            img.thumbnail((300, 300))  # Adjust the size as needed
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk)
            preview_label.image = img_tk
        except Exception as e:
            print(f"Error compressing image: {e}")

# Create the GUI window
window = tk.Tk()
window.title("Image Compressor")

# Add a button to select and compress the image
compress_btn = tk.Button(window, text="Compress Image", command=compress_image)
compress_btn.pack(padx=20, pady=10)

# Add a label to display the compressed image
preview_label = tk.Label(window)
preview_label.pack(padx=20, pady=10)

# Run the GUI application
window.mainloop()

