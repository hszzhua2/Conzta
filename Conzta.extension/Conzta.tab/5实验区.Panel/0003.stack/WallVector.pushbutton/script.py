

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

class WallSelectionFilter(ISelectionFilter):
    def __init__(self):
        pass
    
    def AllowElement(self, element):
        if isinstance(element, Wall):
            return True
        else:
            return False
        
    def AllowReference(self, reference, point):
        return False


doc = __revit__.ActiveUIDocument.Document


wall_filter = WallSelectionFilter()


selected_wall_ref = __revit__.ActiveUIDocument.Selection.PickObject(ObjectType.Element, wall_filter, "Select a wall")


selected_wall = doc.GetElement(selected_wall_ref.ElementId)


wall_curve = selected_wall.Location.Curve


param_value = 0.5 


point_on_curve = wall_curve.Evaluate(param_value, False)


tangent_vector = wall_curve.ComputeDerivatives(param_value, True)[1]


normal_vector = XYZ.BasisZ.CrossProduct(tangent_vector).Normalize()


print("The normal vector of the wall at parameter value", param_value, "is:", normal_vector)
