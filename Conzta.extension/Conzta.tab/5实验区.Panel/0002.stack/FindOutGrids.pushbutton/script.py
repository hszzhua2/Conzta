import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Application, Form, PaintEventArgs

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select wall elements
selection = uidoc.Selection.PickObjects(ObjectType.Element, "Select walls")
wall_ids = [sel.ElementId for sel in selection]
walls = [doc.GetElement(id) for id in wall_ids]

for wall in walls:
    # Check if wall is closed
    wall_location_curve = wall.Location.Curve
    if not wall_location_curve.IsBound:
        print("Walls are not closed!")
    else:
        # Get wall points
        start_point = wall_location_curve.GetEndPoint(0)
        end_point = wall_location_curve.GetEndPoint(1)
        
        # Create polygon
        lines = [Line.CreateBound(start_point, end_point)]
        curve_loop = CurveLoop.Create(lines)



# class PolygonForm(Form):
#     def __init__(self, points):
#         self.points = points
#         self.Paint += self.OnPaint

#     def OnPaint(self, sender, event):
#         graphics = event.Graphics
#         graphics.DrawPolygon(Pens.Black, self.points)

# points = [(100, 100), (200, 100), (200, 200), (100, 200)]
# form = PolygonForm(points)
# Application.Run(form)