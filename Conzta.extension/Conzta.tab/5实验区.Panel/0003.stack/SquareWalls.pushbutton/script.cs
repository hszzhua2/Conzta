using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Collections.Generic;
using System.Linq;

[Transaction(TransactionMode.Manual)]
public class CreateRectangleAndWalls : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        // Get the Revit document and UI application
        UIDocument uiDoc = commandData.Application.ActiveUIDocument;
        Document doc = uiDoc.Document;

        // Get the rectangle's corner points as XYZ coordinates
        XYZ corner1 = new XYZ(0, 0, 0);
        XYZ corner2 = new XYZ(10, 0, 0);
        XYZ corner3 = new XYZ(10, 10, 0);
        XYZ corner4 = new XYZ(0, 10, 0);

        // Create a list of the four corner points
        List<XYZ> corners = new List<XYZ> { corner1, corner2, corner3, corner4 };

        // Get the wall type from the user
        WallType wallType = GetWallTypeFromUser(uiDoc);

        // Create the walls
        List<Wall> walls = CreateWalls(doc, corners, wallType);

        // Return a success message
        message = $"{walls.Count} walls created successfully.";
        return Result.Succeeded;
    }

    private WallType GetWallTypeFromUser(UIDocument uiDoc)
    {
        // Get all wall types in the document
        FilteredElementCollector collector = new FilteredElementCollector(uiDoc.Document);
        List<WallType> wallTypes = collector.OfClass(typeof(WallType)).Cast<WallType>().ToList();

        // Create a form to select the wall type
        SelectWallTypeForm form = new SelectWallTypeForm(wallTypes);

        // Show the form as a dialog
        form.ShowDialog();

        // Return the selected wall type
        return form.SelectedWallType;
    }

    private List<Wall> CreateWalls(Document doc, List<XYZ> corners, WallType wallType)
    {
        // Create a list to hold the created walls
        List<Wall> walls = new List<Wall>();

        // Loop through the corner points and create a wall between each pair of points
        for (int i = 0; i < corners.Count; i++)
        {
            XYZ startPoint = corners[i];
            XYZ endPoint = corners[(i + 1) % corners.Count]; // Wrap around to the first point for the last wall

            // Create a line from the start and end points
            Line line = Line.CreateBound(startPoint, endPoint);

            // Create the wall
            Wall wall = Wall.Create(doc, line, wallType.Id, doc.ActiveView.GenLevel.Id, 10, 0, false, false);

            // Add the wall to the list
            walls.Add(wall);
        }

        // Return the list of walls
        return walls;
    }
}

public class SelectWallTypeForm : System.Windows.Forms.Form
{
    private System.Windows.Forms.Label label1;
    private System.Windows.Forms.ComboBox comboBox1;
    private System.Windows.Forms.Button button1;

    public WallType SelectedWallType { get; private set; }

    public SelectWallTypeForm(List<WallType> wallTypes)
    {
        InitializeComponent();

        // Populate the combo box with the wall types
        comboBox1.DataSource = wallTypes;
        comboBox1.DisplayMember = "Name";
        comboBox1.ValueMember = "Id";
    }

    private void button1_Click(object sender, System.EventArgs e)
{
// Get the selected wall type from the combo box
SelectedWallType = comboBox1.SelectedItem as WallType;

    // Close the form
    Close();
}

private void InitializeComponent()
{
    this.label1 = new System.Windows.Forms.Label();
    this.comboBox1 = new System.Windows.Forms.ComboBox();
    this.button1 = new System.Windows.Forms.Button();
    this.SuspendLayout();
    // 
    // label1
    // 
    this.label1.AutoSize = true;
    this.label1.Location = new System.Drawing.Point(13, 13);
    this.label1.Name = "label1";
    this.label1.Size = new System.Drawing.Size(58, 13);
    this.label1.TabIndex = 0;
    this.label1.Text = "Wall Type:";
    // 
    // comboBox1
    // 
    this.comboBox1.FormattingEnabled = true;
    this.comboBox1.Location = new System.Drawing.Point(77, 10);
    this.comboBox1.Name = "comboBox1";
    this.comboBox1.Size = new System.Drawing.Size(187, 21);
    this.comboBox1.TabIndex = 1;
    // 
    // button1
    // 
    this.button1.Location = new System.Drawing.Point(189, 37);
    this.button1.Name = "button1";
    this.button1.Size = new System.Drawing.Size(75, 23);
    this.button1.TabIndex = 2;
    this.button1.Text = "OK";
    this.button1.UseVisualStyleBackColor = true;
    this.button1.Click += new System.EventHandler(this.button1_Click);
    // 
    // SelectWallTypeForm
    // 
    this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
    this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
    this.ClientSize = new System.Drawing.Size(276, 72);
    this.Controls.Add(this.button1);
    this.Controls.Add(this.comboBox1);
    this.Controls.Add(this.label1);
    this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
    this.MaximizeBox = false;
    this.MinimizeBox = false;
    this.Name = "SelectWallTypeForm";
    this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
    this.Text = "Select Wall Type";
    this.ResumeLayout(false);
    this.PerformLayout();

}
}


