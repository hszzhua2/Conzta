import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import *

# Select CAD line
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

options = Selection.PickObject(ObjectType.Element, "Select a CAD line")
cad_line = doc.GetElement(options.ElementId)

# Locate its layer
cad_layer_id = cad_line.GraphicsStyleId
cad_layer = doc.GetElement(cad_layer_id)

# Select all lines in layer
all_lines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines)
            WhereElementIsNotElementType().ToElements()

layer_lines = []
for line in all_lines:
    if line.GraphicsStyleId == cad_layer_id:
        layer_lines.append(line)

# Create grids based on these lines
for line in layer_lines:
    start = line.GeometryCurve.GetEndPoint(0)
    end = line.GeometryCurve.GetEndPoint(1)
    grid_line = Line.CreateBound(start, end)
    Grid.Create(doc, grid_line)
