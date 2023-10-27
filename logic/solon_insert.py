import csv
import os
from tkinter import messagebox
from ui.solon_show_data import show_data
from logic.reminder import reminder_shown
from logic.solon_load import load_csv
# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')


# Function to insert data into the CSV file
def insert_data(kat_combobox, gak_entry, year_entry, customer_entry, antidikos_entry, comment_entry, tree):
  global reminder_shown

  kat = kat_combobox.get()
  gak = gak_entry.get()
  year = year_entry.get() 
  customer = customer_entry.get()
  antidikos = antidikos_entry.get()
  comment = comment_entry.get()


  # print(kat, gak, year, customer, antidikos, comment)
  # Check if any of the fields are empty
  if not (gak and year and kat):
    messagebox.showerror("ΣΦΑΛΜΑ", "ΠΡΕΠΕΙ ΝΑ ΣΥΜΠΛΗΡΩΣΕΤΕ ΔΙΚΑΣΤΗΡΙΟ, Γ.Α.Κ., ΚΑΙ ΕΤΟΣ")
    kat_combobox.focus_set()
    reminder_shown = False
    return
  # Validate year
  elif not (int(year) >= 2000 and int(year) <=2100):
    messagebox.showerror("ΣΦΑΛΜΑ", "ΤΟ ΕΤΟΣ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΑΝΑΜΕΣΑ ΣΤΟ 2000 ΚΑΙ ΣΤΟ 2100")
    year_entry.focus_set()
    reminder_shown = False
    return
  # Validate Gak Number
  elif not (int(gak) >= 1 and int(gak) <= 999999):
    messagebox.showerror("ΣΦΑΛΜΑ", "Ο ΓΑΚ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΑΝΑΜΕΣΑ ΣΤΟ 1 ΚΑΙ ΣΤΟ 999999")
    gak_entry.focus_set()
    reminder_shown = False
    return

  # remove spaces for gak and year
  if len(gak.replace(" ", "")) != len(gak):
    print("gak has space")
    gak = gak.strip()
  if len(year.replace(" ", "")) != len(year):
    print("year has space")
    year = year.strip()


  # Check if the reminder prompt has been shown
  if not reminder_shown:
    # Show a reminder message
    messagebox.showinfo("Υπενθύμιση", "Παρακαλώ ελέγξτε ΠΡΟΣΕΚΤΙΚΑ τον ΓΑΚ.")
    # Mark the reminder as shown
    reminder_shown = True
    gak_entry.focus_set()

    return  # Do not proceed with insertion on the first click
  # Open the CSV file in append mode and write new data
  with open(INPATH, 'a', newline='', encoding='utf-8') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([kat, gak, year])

  with open(INFOPATH, 'a', newline='', encoding='utf-8') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([customer, antidikos, comment])

  with open(OUTPATH, 'a', newline='', encoding='utf-8') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(["Δεν έχει γίνει ακόμη αναζήτηση"])

  # Clear the text boxes after data insertion
  kat_combobox.set('')
  gak_entry.delete(0, 'end')
  year_entry.delete(0, 'end')
  customer_entry.delete(0, 'end')
  antidikos_entry.delete(0, 'end')
  comment_entry.delete(0, 'end')
  

  reminder_shown = False

  # Load and display the updated CSV data
  data = load_csv()
  show_data(data, tree)
  # load_csv()