

import clr
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__.Application

def transaction(func):
    def wrapper(*args, **kwargs):
        t = Transaction(doc, "pyRevit")
        t.Start()
        try:
            f = func(*args, **kwargs)
            if f:
                t.Commit()
            else:
                t.RollBack()
        except Exception as e:
            print("Error:%s" % e)
            t.RollBack()
            f = False
        return f

    return wrapper

class pyRevit(object):
    @staticmethod
    def of_class(typeof):
        return FilteredElementCollector(doc).OfClass(typeof).ToElements()

class App(pyRevit):
    def __init__(self):
        self.rooms = [room for room in self.of_class(SpatialElement)
                      if isinstance(room, Architecture.Room) and room.Area == 0]

    @transaction
    def main(self):
        try:
            if self.rooms:
                _ = [doc.Delete(r.Id) for r in self.rooms]
            print("Open Room has been removed.")
            return 1
        except Exception as e:
            print(e)
            return 0

if __name__ == '__main__':
    app = App()
    app.main()

print('Done!')