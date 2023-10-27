import os
import csv
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from logic.read_data import read_data
from logic.solon_search import solon_search
from logic.search_status import start_search_var, cancel_search_var, stop_search

# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')
TEXTS_PATH = os.path.join(parent_dir, 'data', 'cute_texts.csv')


FONT_OPTIONS = ("Arial", 13)

# List of cute texts
cute_texts = []
with open(TEXTS_PATH, 'r', encoding = 'utf-8') as csvfile:
  csvreader = csv.reader(csvfile)
  for row in csvreader:
    cute_texts.append(row[0])

# Update the cute text
def update_cute_text(text_label, progress_window):
  try:
    i = 0
    while not stop_search:
      cute_text = cute_texts[i]
      text_label.set(cute_text)
      i = (i + 1) % len(cute_texts)
      progress_window.update() # update the progress window
      time.sleep(5)
    text_label.set("Η Αναζήτηση Ολοκληρώθηκε Επιτυχώς!")
  except Exception as E:
    print(E)


def start_search(root, tree, timestamp_label, search_time_label, total_searches_label):
  # Open the CSV file and read data - initialize input_data and output_data lists
  input_data = read_data(INPATH)
  
  n = len(input_data)

  # Create the progress window
  progress_window = tk.Toplevel(root)
  progress_window.title("ΑΝΑΖΗΤΗΣΗ")
  progress_window.focus_set()
  # progress_window.iconphoto(True, icon)

  def on_close():
    cancel_search_var()
  # if window closes we stop the search
  progress_window.protocol("WM_DELETE_WINDOW", on_close)

  root_width = root.winfo_screenwidth()
  root_height = root.winfo_height()

  progress_window_width = 450
  progress_window_height = 225

  # Center the progress window on top of the root window
  x = (root_width - progress_window_width) // 2
  y = (root_height - progress_window_height) // 2

  progress_window.geometry(f"{progress_window_width}x{progress_window_height}+{x}+{y}")

  text_label = tk.StringVar()
  text_label.set("Αναζήτηση...")

  cute_text_thread = threading.Thread(target = update_cute_text, args = (text_label, progress_window))
  cute_text_thread.start()

  progress_frame = ttk.Frame(progress_window)
  progress_frame.pack(expand = True, fill = "both")

  progress_label = ttk.Label(progress_frame, textvariable = text_label, font = FONT_OPTIONS)
  progress_label.grid(row = 0, column = 0, sticky = 'nsew')

  progress_var = tk.IntVar()
  progress_bar = ttk.Progressbar(progress_frame, mode = 'determinate', maximum = n + 1, variable = progress_var)
  progress_bar.grid(row = 1, column = 0, padx = 5, pady = 15, sticky = "nswe")
  
  # Configure column and row weights for responsiveness
  progress_frame.columnconfigure(0, weight=1)
  progress_frame.rowconfigure(0, weight=1)

  # Create a new thread for the webscraping part
  try:
    start_search_var()
    search_thread = threading.Thread(target = solon_search, args=(input_data, progress_var, n, progress_window, tree, timestamp_label, search_time_label, total_searches_label))
    search_thread.start()
  except Exception as E:
    print(E)
    messagebox.showerror("Σφάλμα", E)

