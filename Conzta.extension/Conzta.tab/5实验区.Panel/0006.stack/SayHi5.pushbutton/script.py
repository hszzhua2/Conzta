# import revit api
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import math

# get the active document
doc = __revit__.ActiveUIDocument.Document

# get the selected walls
selection = __revit__.ActiveUIDocument.Selection
wall1 = doc.GetElement(selection.GetElementIds()[0])
wall2 = doc.GetElement(selection.GetElementIds()[1])

# get the wall locations as curves
loc1 = wall1.Location.Curve
loc2 = wall2.Location.Curve

# get the start and end points of the curves
p1 = loc1.GetEndPoint(0)
p2 = loc1.GetEndPoint(1)
p3 = loc2.GetEndPoint(0)
p4 = loc2.GetEndPoint(1)

# get the distance between the closest points using math.dist function [^1^][5]
d1 = math.dist(p1, p3)
d2 = math.dist(p1, p4)
d3 = math.dist(p2, p3)
d4 = math.dist(p2, p4)
distance = min(d1, d2, d3, d4)

# print the distance in feet
print("Wall distance is " + str(distance) + " ft")