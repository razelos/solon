import os
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

# Function to edit the data from the CSV files
def edit_data(entry_window, index, prekat, pregak, preyear, kat_combobox, gak_entry, year_entry, customer_entry, antidikos_entry, comment_entry, tree):
  try:
    kat = kat_combobox.get()
    gak = gak_entry.get()
    year = year_entry.get() 
    customer = customer_entry.get()
    antidikos = antidikos_entry.get()
    comment = comment_entry.get()
    # if the search values have remained the same as previous (pre) 
    # there is no reason to change the output data
    if prekat == kat and pregak == gak and preyear == year:
      info_data = read_data(INFOPATH)
      info_data[index] = [customer, antidikos, comment]
      write_data(INFOPATH, info_data)
    else:

      input_data = read_data(INPATH)
      info_data = read_data(INFOPATH)
      output_data = read_data(OUTPATH)

      # remove spaces for gak and year
      if len(gak.replace(" ", "")) != len(gak):
        print("gak has space")
        gak = gak.strip()
      if len(year.replace(" ", "")) != len(year):
        print("year has space")
        year = year.strip()

      input_data[index] = [kat, gak, year]
      info_data[index] = [customer, antidikos, comment]
      output_data[index] = ["Δεν έχει γίνει ακόμα αναζήτηση"]

      write_data(INPATH, input_data)
      write_data(INFOPATH, info_data)
      write_data(OUTPATH, output_data)
      
    entry_window.destroy()
    
    data = load_csv()
    show_data(data, tree)
  except Exception as E:
    print(E)
