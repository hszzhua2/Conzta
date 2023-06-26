using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;

[Transaction(TransactionMode.ReadOnly)]
public class WallDistanceCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        // Get the Revit application and document
        UIApplication uiApp = commandData.Application;
        Document doc = uiApp.ActiveUIDocument.Document;

        // Select two walls
        Reference wallRef1 = uiApp.ActiveUIDocument.Selection.PickObject(ObjectType.Element, new WallSelectionFilter(), "Select first wall");
        Reference wallRef2 = uiApp.ActiveUIDocument.Selection.PickObject(ObjectType.Element, new WallSelectionFilter(), "Select second wall");

        // Get the thickness of the walls
        Wall wall1 = doc.GetElement(wallRef1) as Wall;
        Wall wall2 = doc.GetElement(wallRef2) as Wall;
        double thickness1 = wall1.Width;
        double thickness2 = wall2.Width;

        // Get the endpoints of the walls
        LocationCurve curve1 = wall1.Location as LocationCurve;
        LocationCurve curve2 = wall2.Location as LocationCurve;
        XYZ point1a = curve1.Curve.GetEndPoint(0);
        XYZ point1b = curve1.Curve.GetEndPoint(1);
        XYZ point2a = curve2.Curve.GetEndPoint(0);
        XYZ point2b = curve2.Curve.GetEndPoint(1);

        // Calculate the distance between the walls in meters
        double distance = double.MaxValue;
        distance = UnitUtils.Convert(distance, UnitTypeId.Feet, UnitTypeId.Millimeters);

        // Subtract the thickness of each wall from the distance

        // Display the distance in a message box
        TaskDialog.Show("Wall Distance", "墙间距为" + distance.ToString("F2") + "mm");

        return Result.Succeeded;
    }
}

public class WallSelectionFilter : ISelectionFilter
{
    public bool AllowElement(Element elem)
    {
        return (elem is Wall);
    }

    public bool AllowReference(Reference reference, XYZ position)
    {
        return true;
    }
}
