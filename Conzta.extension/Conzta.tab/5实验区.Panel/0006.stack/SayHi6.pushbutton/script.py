
import pyrevit

print("Loading")


print("...")
print("......")
print(".........")

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# get the selected element id
selection = uidoc.Selection
element_id = selection.GetElementIds()[0]
# convert the element id to a string
element_id_str = element_id.ToString()


print("ElenentId is",element_id_str)



print("Done!!!")
