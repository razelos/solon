import os
import datetime
import csv

# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
TIMEPATH = os.path.join(parent_dir, 'data', 'timestamps.csv')


# save time stamp in csv file
def time_stamp(searches):
  try:
    timestamp = datetime.datetime.now()
    timestamp_str = timestamp.strftime("%d-%m-%Y %H:%M:%S")

    # # Convert start_time and end_time strings to datetime objects
    # start_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S")
    # end_time = datetime.datetime.strptime(end_time_str, "%H:%M:%S")

    # search_time = end_time - start_time

    # previous_search_time_str = "00:00:00" # default
    previous_searches = 0 # default
    with open(TIMEPATH, 'r', encoding = 'utf-8') as csvfile:
      csvreader = csv.reader(csvfile)
      rows = list(csvreader)
      if len(rows) >=1 :
          previous_searches = int(rows[1][0])
    
    # # Convert the previous total search time to a timedelta object
    # previous_search_time_parts = previous_search_time_str.split(':')
    # previous_search_time = datetime.timedelta(
    #   hours=int(previous_search_time_parts[0]),
    #   minutes=int(previous_search_time_parts[1]),
    #   seconds=int(previous_search_time_parts[2])
    # )

    # # Calculate the new total search time
    # new_total_search_time = previous_search_time + search_time

    # # Format the search times as "%H:%M:%S"
    # new_total_search_time_str = str(new_total_search_time)

    total_searches = previous_searches + searches

    with open(TIMEPATH, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([timestamp_str])
      writer.writerow([total_searches])
  except Exception as E:
    print("timestamp", E)

# get the timestamp from the csv file
def get_timestamp():
  with open(TIMEPATH, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    row = list(reader)
    if len(row) == 2:
      return row[0], row[1]
    else:
      return "Καμία αναζήτηση ακόμα", "0"
    
# calculate the time that you have saved using this app 
def saved_time(search_count):
  # Calculate the total time in seconds
  # Each search saves you 30 seconds!
  search_count = int(search_count)
  total_seconds = search_count * 30
  
  # Create a timedelta object with the total seconds
  time_delta = datetime.timedelta(seconds=total_seconds)
  
  # Get the hours, minutes, and seconds from the timedelta
  hours, remainder = divmod(time_delta.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)

  return str(hours), str(minutes)