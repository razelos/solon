import os
from functools import partial
import tkinter as tk
from tkinter import  ttk
from tkinter import messagebox
from logic.solon_load import load_csv
from logic.read_data import read_data
from logic.write_data import write_data
from ui.solon_show_data import show_data

# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')

FONT_OPTIONS = ("Arial", 13)# Function to delete data from both input and output CSV files
def delete_data(tree, root):
  try:
    # get the selected row
    row_to_delete = tree.selection()
    if not row_to_delete:
      messagebox.showerror("ΣΦΑΛΜΑ", "ΠΑΡΑΚΑΛΩ ΕΠΙΛΕΞΤΕ ΓΡΑΜΜΗ ΓΙΑ ΔΙΑΓΡΑΦΗ")
      return
    else:

      entry_window = tk.Toplevel(root)
      entry_window.title("ΔΙΑΓΡΑΦΗ ΔΕΔΟΜΕΝΩΝ")
      root_width = root.winfo_screenwidth()
      root_height = root.winfo_height()

      # entry_window.iconphoto(True, icon)

      entry_window_width = 500
      entry_window_height = 250

      # Center the progress window on top of the root window
      x = (root_width - entry_window_width) // 2
      y = (root_height - entry_window_height) // 2
      entry_window.geometry(f"{entry_window_width}x{entry_window_height}+{x}+{y}")

      entry_frame = ttk.Frame(entry_window)
      entry_frame.pack()

      # Focus on the window
      entry_frame.focus_set()

      # get the index of the selected row
      index = tree.index(row_to_delete)

      # Open the CSV file and read data
      input_data = read_data(INPATH)
      info_data = read_data(INFOPATH)
      output_data = read_data(OUTPATH)

      # Entry Fields for Data Insertion
      kat_label = ttk.Label(entry_frame, text="ΔΙΚΑΣΤΗΡΙΟ: " + str(input_data[index][0]), font = FONT_OPTIONS)
      kat_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')

      gak_label = ttk.Label(entry_frame, text="ΓΑΚ: " + str(input_data[index][1]), font = FONT_OPTIONS)
      gak_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

      year_label = ttk.Label(entry_frame, text="ΕΤΟΣ: " + str(input_data[index][2]), font = FONT_OPTIONS)
      year_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

      customer_label = ttk.Label(entry_frame, text="ΠΕΛΑΤΗΣ: " + str(info_data[index][0]), font = FONT_OPTIONS)
      customer_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

      antidikos_label = ttk.Label(entry_frame, text="ΑΝΤΙΔΙΚΟΣ: " + str(info_data[index][1]), font = FONT_OPTIONS)
      antidikos_label.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')

      comment_label = ttk.Label(entry_frame, text="ΣΧΟΛΙΑ: " + str(info_data[index][2]), font = FONT_OPTIONS)
      comment_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

      def delete_confirm(input_data, info_data, output_data, index, entry_window, tree):
        input_data.pop(index)
        info_data.pop(index)
        output_data.pop(index)
        # Write the updated data back to their respective files
        write_data(INPATH, input_data)
        write_data(INFOPATH, info_data)
        write_data(OUTPATH, output_data)
        entry_window.destroy()
        data = load_csv()
        show_data(data, tree)
      
      def close(entry_window):
        entry_window.destroy()

      delete_button = ttk.Button(entry_frame, text="ΔΙΑΓΡΑΦΗ", style = "Delete.TButton", command =  partial(delete_confirm, input_data, info_data, output_data, index, entry_window, tree))
      delete_button.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 5)
      cancel_button = ttk.Button(entry_frame, text="ΑΚΥΡΩΣΗ", style = "Insert.TButton", command =  partial(close, entry_window))
      cancel_button.grid(row = 6, column = 1, columnspan = 2, padx = 10, pady = 5)

  except Exception as E:
    print(E)
