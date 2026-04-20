import tkinter as tk
from tkinter import filedialog, scrolledtext
from google.cloud import vision
from google.oauth2 import service_account
import os

# Get the folder where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the JSON key in the same folder
KEY_PATH = os.path.join(BASE_DIR, "service-account-key.json")

# Load credentials
creds = service_account.Credentials.from_service_account_file(KEY_PATH)

# Create Vision API client
client = vision.ImageAnnotatorClient(credentials=creds)

# global (store selected image path)
selected_image_path = None

def choose_image():
    global selected_image_path
    path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp *.gif")]
    )
    if path:
        selected_image_path = path
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"Selected image:\n{path}\n")

def process_image():
    if not selected_image_path:
        output_box.insert(tk.END, "\nNo image selected.\n")
        return

    with open(selected_image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # label detection
    labels = client.label_detection(image=image).label_annotations

    # text detection
    text_response = client.text_detection(image=image)
    extracted_text = ""
    if text_response.text_annotations:
        extracted_text = text_response.text_annotations[0].description

    # output the results
    output_box.insert(tk.END, "\nClassification Labels:\n")
    for label in labels:
        output_box.insert(tk.END, f"{label.description} ({label.score:.2f})\n")

    output_box.insert(tk.END, "\nExtracted Text:\n")
    output_box.insert(tk.END, extracted_text + "\n")

# ---- TKinter GUI ----

root = tk.Tk()
root.title("AI Stock Classifier Demo")
root.geometry("600x500")

choose_btn = tk.Button(root, text="Choose Image", command=choose_image)
choose_btn.pack(pady=10)

process_btn = tk.Button(root, text="Submit to Cloud Vision API", command=process_image)
process_btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, width=70, height=25)
output_box.pack(pady=10)

root.mainloop()
