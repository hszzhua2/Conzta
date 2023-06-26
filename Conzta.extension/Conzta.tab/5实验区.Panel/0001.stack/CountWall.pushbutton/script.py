import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

doc = __revit__.ActiveUIDocument.Document

walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

wall_count = len(walls)

print("Number of walls in the file: {}".format(wall_count))


window_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()
door_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()

window_type_count = len(window_types)
door_type_count = len(door_types)
total_count = window_type_count + door_type_count

print("Number of window types: {}".format(window_type_count))
print("Number of door types: {}".format(door_type_count))
print("Total number of window and door types: {}".format(total_count))