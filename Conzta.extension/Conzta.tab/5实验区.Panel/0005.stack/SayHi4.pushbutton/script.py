print("Loading...")
import pyrevit
import sys
sys.path.append(r"C:\Users\zhuangzefeng\AppData\Roaming\pyRevit-Master\site-packages")

try:
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')

    from Autodesk.Revit.DB import *

    doc = __revit__.ActiveUIDocument.Document
    floors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()

    total_area = 0.0

    for floor in floors:
        area_param = floor.LookupParameter('Area')
        if area_param:
            area = area_param.AsDouble()
            total_area += area

    print('Total floor area:', total_area, 'square feet')



    
except:
    print(".....Error!!")