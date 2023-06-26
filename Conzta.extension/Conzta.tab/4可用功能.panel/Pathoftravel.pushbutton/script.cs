using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Analysis;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.DB.Mechanical;
using Autodesk.Revit.DB.Electrical;
using Autodesk.Revit.DB.Plumbing;
using Autodesk.Revit.DB.Structure;
using System.Collections;


namespace 一点到多房间pathoftravel
{
    [Transaction(TransactionMode.Manual)]
    public class PathOfTravelCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            UIDocument uidoc = commandData.Application.ActiveUIDocument;
            Document doc = uidoc.Document;

            try
            {
                // Get all room elements
                FilteredElementCollector collector = new FilteredElementCollector(doc);
                ICollection<Element> rooms = collector.OfClass(typeof(SpatialElement)).OfCategory(BuiltInCategory.OST_Rooms).ToElements();

                // Create array to store all room location points
                List<XYZ> roomPoints = new List<XYZ>();

                // Iterate through each room element and get its location point
                foreach (Element room in rooms)
                {
                    SpatialElement spatialElement = room as SpatialElement;
                    LocationPoint locationPoint = room.Location as LocationPoint;

                    // Check if locationPoint is not null before accessing its properties
                    if (locationPoint != null)
                    {
                        XYZ roomLocation = locationPoint.Point;
                        roomPoints.Add(roomLocation);
                    }
                }

                // Flatten the list of room location points
                List<XYZ> flattenedRoomPoints = roomPoints.SelectMany(x => x is IList ? ((IList)x).Cast<XYZ>() : new List<XYZ> { x }).ToList();

                // Create path of travel
                using (Transaction t = new Transaction(doc, "Create Path of Travel"))
                {
                    t.Start();

                    // Use the first room location point as the starting point
                    XYZ firstPoint = uidoc.Selection.PickPoint("Select first point for Path of Travel");

                    // Iterate through all room location points and connect them in order
                    for (int i = 0; i < flattenedRoomPoints.Count; i++)
                    {
                        if (i == 0) continue; // Skip the first room location point since it's the starting point

                        XYZ endPoint = flattenedRoomPoints[i];
                        PathOfTravel.Create(doc.ActiveView, firstPoint, endPoint);
                    }

                    t.Commit();
                }

                return Result.Succeeded;
            }
            catch (Autodesk.Revit.Exceptions.OperationCanceledException)
            {
                return Result.Cancelled;
            }
        }
    }
}

