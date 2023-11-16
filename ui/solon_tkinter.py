import tkinter as tk
from tkinter import  ttk
import os
from tkinter import messagebox
from functools import partial
import csv
def run():

  from logic.solon_insert import insert_data
  from logic.solon_load import load_csv, read_data
  from logic.solon_edit import edit_data
  from logic.solon_delete import delete_data
  from ui.solon_show_data import show_data
  from ui.start_search import start_search
  from logic.timestamp import get_timestamp, saved_time

  # File Paths that are needed 
  # Get the current directory of your script
  current_dir = os.path.dirname(__file__)

  # Navigate up one level to the parent directory, which is 'solon search'
  parent_dir = os.path.dirname(current_dir)

  # Define the path to the 'info.csv' file in the 'data' folder
  INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
  INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
  OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')
  KATPATH = os.path.join(parent_dir, 'data', 'dikastiria.csv')


  # List of court options
  kat_options = []
  with open(KATPATH, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
      kat_options.append(row[0])


  # Function to show the entry fields for data insertion
  def show_fields(type, tree):

    if type =="edit" and not(tree.selection()):
      messagebox.showerror("ΣΦΑΛΜΑ", "ΠΑΡΑΚΑΛΩ ΕΠΙΛΕΞΤΕ ΓΡΑΜΜΗ ΓΙΑ ΕΠΕΞΕΡΓΑΣΙΑ")
      return
    # Entry Window
    entry_window = tk.Toplevel(root)
    if type == "insert":
      entry_window.title("ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ")
    elif type == "edit":
      entry_window.title("ΕΠΕΞΕΡΓΑΣΙΑ ΔΕΔΟΜΕΝΩΝ")
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

    # Entry Fields for Data Insertion
    kat_label = ttk.Label(entry_frame, text="ΔΙΚΑΣΤΗΡΙΟ:", font = FONT_OPTIONS)
    kat_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')
    kat_combobox = ttk.Combobox(entry_frame, values = kat_options, state="readonly", font = FONT_OPTIONS)
    kat_combobox.grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = 5)

    gak_label = ttk.Label(entry_frame, text="ΓΑΚ:", font = FONT_OPTIONS)
    gak_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')
    gak_entry = ttk.Entry(entry_frame, font = FONT_OPTIONS)
    gak_entry.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 5)

    year_label = ttk.Label(entry_frame, text="ΕΤΟΣ:", font = FONT_OPTIONS)
    year_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')
    year_entry = ttk.Entry(entry_frame, font = FONT_OPTIONS)
    year_entry.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 5)

    customer_label = ttk.Label(entry_frame, text="ΠΕΛΑΤΗΣ: ", font = FONT_OPTIONS)
    customer_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')
    customer_entry = ttk.Entry(entry_frame, font = FONT_OPTIONS)
    customer_entry.grid(row = 3, column = 1, padx = 10, pady = 5)

    antidikos_label = ttk.Label(entry_frame, text="ΑΝΤΙΔΙΚΟΣ: ", font = FONT_OPTIONS)
    antidikos_label.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')
    antidikos_entry = ttk.Entry(entry_frame, font = FONT_OPTIONS)
    antidikos_entry.grid(row = 4, column = 1, padx = 10, pady = 5)

    comment_label = ttk.Label(entry_frame, text="ΣΧΟΛΙΑ: ", font = FONT_OPTIONS)
    comment_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')
    comment_entry = ttk.Entry(entry_frame, font = FONT_OPTIONS)
    comment_entry.grid(row = 5, column = 1, padx = 10, pady = 5)

    if type == "insert":

      insert_button = ttk.Button(entry_frame, text="ΕΙΣΑΓΩΓΗ", style = "Insert.TButton", command= partial(insert_data, kat_combobox, gak_entry, year_entry, customer_entry, antidikos_entry, comment_entry, tree))
      insert_button.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 5)

    elif type == "edit":
      try:
        # get the selected row
        row_to_edit = tree.selection()
        index = tree.index(row_to_edit)

        # read the data that is needed
        input_data = read_data(INPATH)
        info_data = read_data(INFOPATH)

        kat = input_data[index][0]
        gak = input_data[index][1]
        year = input_data[index][2]
        customer = info_data[index][0]
        antidikos = info_data[index][1]
        comment = info_data[index][2]
        
        # fill out the fields with the values
        kat_combobox.set(kat)
        gak_entry.insert(0, gak)
        year_entry.insert(0, year)
        customer_entry.insert(0, customer)
        antidikos_entry.insert(0, antidikos)
        comment_entry.insert(0, comment)

        save_edit_button = ttk.Button(entry_frame, text="ΑΠΟΘΗΚΕΥΣΗ", style = "Edit.TButton", command = partial(edit_data, entry_window, index, kat, gak, year, kat_combobox, gak_entry, year_entry, customer_entry, antidikos_entry, comment_entry, tree))
        save_edit_button.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 5)

      except Exception as E:
        print(E)

  # Layout-----------------------------

  # Define custom colors using hexadecimal color codes - these are not actively used except
  # for the background color for the root window which is light gray by default
  BACKGROUND_COLOR = "#F0F0F0"  # Light Gray
  # PRIMARY_COLOR = "#007ACC"  # Blue
  # SECONDARY_COLOR = "#FFA500"  # Orange

  # Define Font options for the Text
  FONT_OPTIONS = ("Arial", 13)


  root = tk.Tk()
  root.title("Solon Search")
  # Configure the root window's background color
  root.configure(background=BACKGROUND_COLOR)

  # Load the icon file
  # icon = tk.PhotoImage(file = "./test.png")
  # root.iconphoto(True, icon)

  # Get the screen width and height
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()

  window_width = 1100
  window_height = 650

  # Calculate the x and y coordinates for the center of the screen
  x = (screen_width - window_width) // 2
  y = (screen_height - window_height) // 2

  # Set the geometry of the root window to open it in the center of the screen
  root.geometry(f"{window_width}x{window_height}+{x}+{y}")


  global timestamp_label, search_time_label, total_searches_label

  # Treeview to display CSV data

  # Also includes Button Frame and deselect function so 
  # user can deselect rows
  # def tree(root, timestamp_label, search_time_label, total_searches_label):
  def tree(root):
    tree_style = ttk.Style()
    tree_style.configure("Custom.Treeview", rowheight = 30, font = FONT_OPTIONS)
    tree = ttk.Treeview(root, columns=("Kat", "Gak", "Year", "Customer", "Antidikos", "Comment", "Result"), show="headings", style = "Custom.Treeview")

    # Set column widths (adjust these values as needed)
    tree.column("#1", width=220)  # First column
    tree.column("#2", width=60)  # Second column
    tree.column("#3", width=60)   # Third column
    tree.column("#4", width=170)   # Third column
    tree.column("#5", width=170)   # Third column
    tree.column("#6", width=150)   # Third column
    tree.column("#7", width=250)  # Seventh column

    # Function to change the font of Treeview headings
    def change_heading_font(font):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=font)

    # Apply the custom font to the headings
    change_heading_font(("open sans", 14))

    tree.heading("Kat", text="ΔΙΚΑΣΤΗΡΙΟ", anchor = "w")
    tree.heading("Gak", text="ΓΑΚ", anchor = "w")
    tree.heading("Year", text="ΕΤΟΣ", anchor = "w")
    tree.heading("Customer", text="ΠΕΛΑΤΗΣ", anchor = 'w')
    tree.heading("Antidikos", text="ΑΝΤΙΔΙΚΟΣ", anchor = 'w')
    tree.heading("Comment", text="ΣΧΟΛΙΑ", anchor = 'w')
    tree.heading("Result", text="ΑΠΟΦΑΣΗ", anchor = "w")

    # Create a vertical scrollbar
    vscrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vscrollbar.pack(side="right", fill="y")

    # Configure the Treeview to use the vertical scrollbar
    tree.configure(yscrollcommand=vscrollbar.set)

    data = load_csv()
    show_data(data, tree)

    tree.pack()
    # Button Frame
    def button_frame(root):
      button_frame = ttk.Frame(root)
      button_frame.pack(side='top', pady = 20)

      # Button to Insert Data
      insbutton_style = ttk.Style()
      insbutton_style.configure("Insert.TButton", font = (FONT_OPTIONS), background = 'green', foreground='black')
      insbutton = ttk.Button(button_frame, text="ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ", style = "Insert.TButton", command= partial(show_fields, "insert", tree))
      insbutton.grid(row = 0, column = 0, padx = 10, pady = 5)

      # Edit Button
      editbutton_style = ttk.Style()
      editbutton_style.configure("Edit.TButton", font = (FONT_OPTIONS), background = 'orange', foreground = 'black')
      edit_button = ttk.Button(button_frame, text = 'ΕΠΕΞΕΡΓΑΣΙΑ', style = "Edit.TButton", command = partial(show_fields, "edit", tree))
      edit_button.grid(row = 0, column = 1, padx = 10, pady = 5)

      # Delete Button
      delbutton_style = ttk.Style()
      delbutton_style.configure("Delete.TButton", font = (FONT_OPTIONS), background = 'red', foreground = 'black')
      delete_button = ttk.Button(button_frame, text="ΔΙΑΓΡΑΦΗ ΔΕΔΟΜΕΝΩΝ", style = "Delete.TButton", command = partial(delete_data, tree, root))
      # delete_button = ttk.Button(button_frame, text="ΔΙΑΓΡΑΦΗ ΔΕΔΟΜΕΝΩΝ", style = "Delete.TButton", command = partial(show_fields,"delete", tree))
      delete_button.grid(row = 0, column = 2, padx = 10, pady = 5)

      # Search Button
      searchbutton_style = ttk.Style()
      searchbutton_style.configure("Search.TButton", font = (FONT_OPTIONS), background = 'blue', foreground = 'black')
      global timestamp_label, search_time_label, total_searches_label
      search_button = ttk.Button(button_frame, text="ΑΝΑΖΗΤΗΣΗ", style = "Search.TButton", command = partial(start_search, root, tree, timestamp_label, search_time_label, total_searches_label))
      search_button.grid(row = 0, column = 3, padx = 10, pady = 5)
      return edit_button, delete_button

    edit_button, delete_button = button_frame(root)
    # Function to unselect the currently selected row in the Treeview
    def unselect_tree_row(event):
      # not clicked on delete button
      if event.widget == delete_button:
          return
      # not clicked on edit button
      elif event.widget == edit_button:
          return
      # not clicked on other point in tree
      elif event.widget != tree:
        tree.selection_remove(tree.selection())
    # Bind the click event on the root window to unselect the Treeview row
    root.bind("<Button-1>", unselect_tree_row)


  # Set up the time Frame
  def time_frame(root):


    time_frame = ttk.Frame(root)
    # time_frame.pack(side = 'top', pady = 10)

    timestamp, total_searches = get_timestamp()
    hours, minutes = saved_time(total_searches[0])
    global timestamp_label, search_time_label, total_searches_label
    timestamp_label = tk.Label(time_frame, text="ΤΕΛΕΥΤΑΙΑ ΑΝΑΖΗΤΗΣΗ: " + timestamp[0], font = FONT_OPTIONS)
    timestamp_label.grid(row = 0, pady = 0)
    search_time_label = tk.Label(time_frame, text = "ΕΧΕΤΕ ΓΛΥΤΩΣΕΙ ΣΥΝΟΛΙΚΑ " + hours + " ΩΡΕΣ ΚΑΙ " + minutes + " ΛΕΠΤΑ ΑΝΑΖΗΤΗΣΗΣ!", font = ("open sans", 9))
    search_time_label.grid(row = 1, pady = 0)
    total_searches_label = tk.Label(time_frame, text = "ΕΧΕΤΕ ΠΡΑΓΜΑΤΟΠΟΙΗΣΕΙ ΣΥΝΟΛΙΚΑ " + total_searches[0] + " ΑΝΑΖΗΤΗΣΕΙΣ", font = ("open sans", 9))
    total_searches_label.grid(row = 2, pady = 0)
    return time_frame

  # Set up the adbox
  def adbox_frame(root):
    adbox_frame = ttk.Frame(root)
    adbox_frame.pack(side = 'bottom', pady = 20)

    adbox_label = tk.Label(adbox_frame, text = "Νικόλαος Ραζέλος - Πληροφορική για δικηγόρους", font = FONT_OPTIONS)
    adbox_label2 = tk.Label(adbox_frame, text = "example@email.com", font = FONT_OPTIONS)
    adbox_label3 = tk.Label(adbox_frame, text = "694 3755 032", font = FONT_OPTIONS)
    adbox_label.grid(row = 0, column = 0, padx = 10, pady = 5)
    adbox_label2.grid(row = 1, column = 0, padx = 10, pady = 5)
    adbox_label3.grid(row = 2, column = 0, padx = 10, pady = 5)

  timeframe = time_frame(root)
  tree(root)
  timeframe.pack(side = 'top', pady = 10)
  adbox_frame(root)

  root.mainloop()

# run()