using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Windows.Forms;

namespace HelloWorld
{
    [Transaction(TransactionMode.Manual)]
    public class HelloWorldCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            TaskDialog.Show("Hello World!", "睡前原谅一切，醒来便是重生！                   ——Greetings from Revit 2023!");
            return Result.Succeeded;
        }
    }
}
