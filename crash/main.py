import pytesseract
from PIL import Image
import mss
import tkinter as tk
from tkinter import ttk
from datetime import datetime

nowVal = 0
preVal = 0
Data = []

# Ensure Tesseract is installed on your system and set the correct path to the executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def capture_screen(region=None):
    with mss.mss() as sct:
        screenshot = sct.grab(region) if region else sct.grab(sct.monitors[1])
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img

def extract_text_from_image(img):
    # Convert image to grayscale
    gray_img = img.convert('L')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray_img)
    return text

def update_gui():
    global nowVal, preVal

    region = {'left': 1400, 'top': 515, 'width': 300, 'height': 115}
    screenshot = capture_screen(region)
    text = extract_text_from_image(screenshot)

    if "x" in text:
        print("Extracted Text:" + text)
        
        try:
            nowVal = float(text[0:4])
        except ValueError:
            print("Conversion failed!")

        if preVal > nowVal:
            Data.append(preVal)
            print("Data: ", Data)
            append_data_to_file(preVal, 'data.txt')

        preVal = nowVal

    # Update the GUI with the current value and data list
    current_value_label.config(text=f"Current Value: {nowVal}")
    data_list_text.delete(1.0, tk.END)
    for item in Data:
        data_list_text.insert(tk.END, f"{datetime.now()}: {item}\n")
    
    # Schedule the update_gui function to run again after 1000 milliseconds (1 second)
    root.after(1000, update_gui)

def append_data_to_file(data, filename):
    with open(filename, 'a') as file:
        file.write(f"{datetime.now()}: {data}\n")

# Create the main application window
root = tk.Tk()
root.title("1XBet Value Extractor")
root.geometry("400x1000")
root.configure(bg='black')

# Create and pack the current value label
current_value_label = tk.Label(root, text="Current Value: ", fg='green', bg='black', font=('Unispace', 17))
current_value_label.pack(pady=10)

# Create and pack the data list text widget
data_list_text = tk.Text(root, fg='green', bg='black', font=('Unispace', 17), height=40)
data_list_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Start the GUI update loop
root.after(5000, update_gui)

# Start the tkinter main loop
root.mainloop()
