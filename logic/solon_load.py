import os
from logic.read_data import read_data

# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')


# Function to load the data from the CSV file
def load_csv():
  try:
    # Open the CSV file and read data
    input_data = read_data(INPATH)
    info_data = read_data(INFOPATH)
    output_data = read_data(OUTPATH)

    # If some mistake and  len(input_data) != len(output_data) then fix it
    if len(input_data) > len(output_data):
      for i in range(len(output_data)):
        if len(output_data[i]) == 0:
          output_data[i] = "ΥΠΗΡΞΕ ΚΑΠΟΙΟ ΣΦΑΛΜΑ"
      for i in range(len(output_data), len(input_data)):
        output_data.append(["ΥΠΗΡΞΕ ΚΑΠΟΙΟ ΣΦΑΛΜΑ"])

    # Insert CSV data into the treeview
    combined_row = []
    for i in range(len(input_data)):
      combined_row.append(input_data[i] + info_data[i] + output_data[i])
    # print(combined_row)
    return combined_row
  except Exception as E:
    print(E)
    # print(input_data[i], info_data[i], output_data[i])
    # print(combined_row)

load_csv()