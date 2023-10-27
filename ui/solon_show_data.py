# Custom cell renderer function to apply background color based on text content
def cell_background_color(cell_data):
  # Determine the tag based on the text content
  if "ΕΚΚΡΕΜΕΙ" in cell_data:
    return "red"
  elif "ΕΛΕΓΞΤΕ" in cell_data:
    return "orange"
  elif "ΥΠΗΡΞΕ" in cell_data:
    return "yellow"
  elif "Δεν έχει" in cell_data:
    return "lightgray"
  else:
    return "green"

def show_data(data, tree):
  # Clear the existing data in the treeview
  for row in tree.get_children():
      tree.delete(row)

  # Define tag configurations for different background colors
  tree.tag_configure("red", background="#E10600")
  tree.tag_configure("orange", background="orange")
  tree.tag_configure("yellow", background="yellow")
  tree.tag_configure("green", background="lightgreen")
  tree.tag_configure("lightgray", background="#F0F0F0")

  for i in range(len(data)):
    tag = cell_background_color(data[i][6])
    tree.insert("", "end", values=(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]), tags=(tag))
