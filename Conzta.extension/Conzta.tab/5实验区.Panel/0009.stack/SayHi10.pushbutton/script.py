import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('System.Windows.Forms')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Windows.Forms import *

# Define a function to change the wall type
def change_wall_type(wall, new_type):
    wall.WallType = new_type

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Get all the wall types in the document
wall_types = FilteredElementCollector(doc).OfClass(WallType).ToElements()

# Create a form to select the wall type
form = Form()
form.Text = "Select Wall Type"

# Create a list box to display the wall types
list_box = ListBox()
list_box.SelectionMode = SelectionMode.MultiSimple
list_box.Dock = DockStyle.Fill

# Add the wall types to the list box
for wall_type in wall_types:
    list_box.Items.Add(wall_type.Name)

# Add the list box to the form
form.Controls.Add(list_box)

# Create a button to change the wall types
button = Button()
button.Text = "OK"
button.Dock = DockStyle.Bottom

# Add an event handler to the button
def button_click(sender, args):
    # Get the selected wall types
    selected_types = []
    for item in list_box.SelectedItems:
        selected_types.append(item)

    # Get all the walls in the document
    walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()

    # Loop through the walls and change the wall type if it is in the selected types
    for wall in walls:
        if wall.WallType.Name in selected_types:
            new_type = wall_types[selected_types.index(wall.WallType.Name)]
            change_wall_type(wall, new_type)

    # Close the form
    form.Close()

button.Click += button_click

# Add the button to the form
form.Controls.Add(button)

# Show the form
form.ShowDialog()