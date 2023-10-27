import csv
# Open the CSV file and write data
def write_data(filepath, data):
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)