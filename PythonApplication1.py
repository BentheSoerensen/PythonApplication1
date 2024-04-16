import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

filename = ""  # Define filename as a global variable

def browse_file():
    global filename  # Access the global filename variable
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, shorten_path(filename))

def shorten_path(path, length=40):
    if len(path) <= length:
        return path
    else:
        parts = path.split("/")
        return ".../" + "/".join(parts[-(length//2):])

def read_file():
    global filename  # Access the global filename variable
    try:
        if filename:
            

            # Read the image
            image = cv2.imread(filename)

            # Get the dimensions of the image
            height, width, _ = image.shape

            # Calculate the total number of pixels
            num_pixels_original = height * width

            # Convert the image to the HSV color space
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Split the HSV image into individual channels
            h, s, v = cv2.split(hsv_image)

            # Threshold the Saturation channel to create a binary mask
            _, saturation_mask = cv2.threshold(s, 20, 255, cv2.THRESH_BINARY_INV)  # Threshold value set to 100

            # Count the number of pixels below the threshold in the Saturation channel
            num_pixels_below_threshold = cv2.countNonZero(saturation_mask)

            # Calculate the percentage of pixels below the threshold compared with the original number of pixels
            percentage_below_threshold = (num_pixels_below_threshold / num_pixels_original) * 100
            percentage_above_threshold = 100 - percentage_below_threshold

            # Update the label with the percentage above threshold
            percentage_label.config(text=f"Percentage of Pixels above Threshold: {percentage_above_threshold:.2f}%")
        else:
            print("Please select a file.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

def exit_app():
    root.destroy()  # Close the tkinter window

# Create the main window
root = tk.Tk()
root.title("File Input")

# Load the background image
try:
    bg_image = Image.open("c:/danialogo.png")  # Make sure the file path is correct and the image file exists
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.grid(row=0, column=0, columnspan=8, rowspan=8, sticky="nsew")
except FileNotFoundError:
    print("Background image file not found.")
except Exception as e:
    print("Error loading background image:", e)

# Create a label
label = tk.Label(root, text="Enter file path:")
label.grid(row=8, column=0)

# Create a text entry widget
entry = tk.Entry(root, width=50)
entry.grid(row=6, column=1, columnspan=4)

# Create a button to browse for the file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=6, column=5)

# Create a button to read the file
read_button = tk.Button(root, text="Read File", command=read_file)
read_button.grid(row=8, column=6)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.grid(row=8, column=7)

# Create a label to display the percentage of pixels above threshold
percentage_label = tk.Label(root, text="")
percentage_label.grid(row=9, column=0, columnspan=8)

# Start the main event loop
root.mainloop()

