using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

[Transaction(TransactionMode.Manual)]
public class SelectAndGetBoundingBox : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        UIDocument uiDoc = commandData.Application.ActiveUIDocument;
        Document doc = uiDoc.Document;

        // Prompt the user to select an element
        Reference selectedRef = uiDoc.Selection.PickObject(ObjectType.Element);

        // Get the selected element
        Element selectedElem = doc.GetElement(selectedRef);

        // Get the bounding box of the selected element
        BoundingBoxXYZ bbox = selectedElem.get_BoundingBox(null);

        // Display the bounding box dimensions
        double length = bbox.Max.X - bbox.Min.X;
        double width = bbox.Max.Y - bbox.Min.Y;
        double height = bbox.Max.Z - bbox.Min.Z;

        TaskDialog.Show("Selected Element Bounding Box", $"Length: {length}, Width: {width}, Height: {height}");

        return Result.Succeeded;
    }
}
