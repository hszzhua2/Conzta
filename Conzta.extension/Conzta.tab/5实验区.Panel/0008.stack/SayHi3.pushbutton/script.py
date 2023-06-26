print("Loading...")
print("...")
print("......")
print(".........")
import pyrevit
import sys
import os
sys.path.append(r"C:\Users\zhuangzefeng\AppData\Roaming\pyRevit-Master\site-packages")
try:
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    from Autodesk.Revit.DB import *

    def get_all_rooms(doc):
        collector = FilteredElementCollector(doc)
        rooms = collector.OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
        return rooms

    def get_room_area(room):
        area = 0
        for boundary in room.GetBoundarySegments(SpatialElementBoundaryOptions()):
            for segment in boundary:
                area += segment.GetCurve().Length
        return area / 304.8 ** 2
        return area / 1000000  # convert from square millimeters to square meters

    doc = __revit__.ActiveUIDocument.Document
    rooms = get_all_rooms(doc)
    total_area = 0
    for room in rooms:
        total_area += get_room_area(room)

    print('Total room area:', total_area, 'sq ft')



    print(sys.executable)
    print(sys.prefix)
    print("...")
    print("......")
    print(".........")
    
    mp3_file = r"C:\Users\zhuangzefeng\Downloads\aigei_com.mp3"
    potplayer_exe = r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe"

    if os.path.exists(mp3_file):
        os.system('"%s" "%s"' % (potplayer_exe, mp3_file))
    print("Finished!!")
except:
    print(".....Error!!")

    
