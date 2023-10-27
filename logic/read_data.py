import csv
# Open the CSV file and read data
def read_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)
    return data