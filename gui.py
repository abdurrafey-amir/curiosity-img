import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import main  # Import the mars_rover_api module

def fetch_images():
    date = date_entry.get()
    file_name = file_entry.get()
    main.mars_rover_photos(file_name, date)  # Call the mars_rover_photos function from the mars_rover_api module

window = tk.Tk()
window.title("Mars Rover Image Fetcher")

date_label = tk.Label(window, text="Enter Date (YYYY-MM-DD):")
date_label.pack()
date_entry = tk.Entry(window)
date_entry.pack()

file_label = tk.Label(window, text="Enter File Name (.txt):")
file_label.pack()
file_entry = tk.Entry(window)
file_entry.pack()

fetch_button = tk.Button(window, text="Fetch Images", command=fetch_images)
fetch_button.pack()

window.mainloop()
