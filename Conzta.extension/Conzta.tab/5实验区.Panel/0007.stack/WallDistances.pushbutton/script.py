import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.DB.Structure import *

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

ref = uidoc.Selection.PickObject(ObjectType.Element, "Select first wall element")
wall1 = doc.GetElement(ref.ElementId)

# Retrieve the wall curve and length in meters
if wall1:
    curve = wall1.Location.Curve
    length = curve.Length * 0.3048 # convert feet to meters
    print("Wall Curve: ", curve)
    print("Wall Length: ", length, "m")
else:
    print("Please select a wall element.")
