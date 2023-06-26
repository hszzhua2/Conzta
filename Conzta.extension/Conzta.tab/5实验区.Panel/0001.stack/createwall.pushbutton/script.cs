using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Collections.Generic;

namespace RevitAddIn
{
    [Transaction(TransactionMode.Manual)]
    public class CreateWallCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            // Get the current Revit document and UIDocument
            UIDocument uidoc = commandData.Application.ActiveUIDocument;
            Document doc = uidoc.Document;

            // Get all wall types in the current Revit file
            FilteredElementCollector wallTypeCollector = new FilteredElementCollector(doc);
            IList<Element> wallTypes = wallTypeCollector.OfClass(typeof(WallType)).ToElements();

            // Create a list of wall type names to use for the combobox
            List<string> wallTypeNames = new List<string>();
            foreach (Element wallType in wallTypes)
            {
                wallTypeNames.Add(wallType.Name);
            }

            // Create the form and add controls
            System.Windows.Forms.Form form = new System.Windows.Forms.Form();
            form.Text = "Create Wall";
            form.Width = 300;
            form.Height = 200;

            System.Windows.Forms.ComboBox wallTypeComboBox = new System.Windows.Forms.ComboBox();
            wallTypeComboBox.Width = 200;
            wallTypeComboBox.Location = new System.Drawing.Point(50, 50);
            wallTypeComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            wallTypeComboBox.Items.AddRange(wallTypeNames.ToArray());
            form.Controls.Add(wallTypeComboBox);

            System.Windows.Forms.Button selectButton = new System.Windows.Forms.Button();
            selectButton.Text = "OK";
            selectButton.Location = new System.Drawing.Point(100, 100);
            selectButton.Click += (sender, e) =>
            {
                try
                {
                    // Get the selected wall type
                    string selectedWallTypeName = wallTypeComboBox.SelectedItem.ToString();
                    WallType selectedWallType = wallTypeCollector.OfClass(typeof(WallType)).FirstElement(wt => wt.Name == selectedWallTypeName) as WallType;

                    // Prompt the user to select the first point
                    XYZ firstPoint = uidoc.Selection.PickPoint("Select the first point of the wall.");

                    // Prompt the user to select the second point
                    XYZ secondPoint = uidoc.Selection.PickPoint("Select the second point of the wall.");

                    // Create the wall using the selected wall type and the two points
                    using (Transaction transaction = new Transaction(doc, "Create Wall"))
                    {
                        transaction.Start();
                        Wall.Create(doc, Line.CreateBound(firstPoint, secondPoint), selectedWallType.Id, doc.ActiveView.GenLevel.Id);
                        transaction.Commit();
                    }

                    // Display a success message
                    TaskDialog.Show("Success", "Wall created successfully.");

                    // Close the form
                    form.DialogResult = System.Windows.Forms.DialogResult.OK;
                    form.Close();
                }
                catch (Autodesk.Revit.Exceptions.OperationCanceledException)
                {
                    // User canceled the operation
                }
                catch (System.Exception ex)
                {
                    // Display an error message if something went wrong
                    TaskDialog.Show("Error", ex.Message);
                }
            };
            form.Controls.Add(selectButton);

            // Show the form
            System.Windows.Forms.DialogResult dialogResult = form.ShowDialog();

            if (dialogResult == System.Windows.Forms.DialogResult.OK)
            {
                return Result.Succeeded;
            }
            else
            {
                return Result.Cancelled;
            }
        }
    }
}
