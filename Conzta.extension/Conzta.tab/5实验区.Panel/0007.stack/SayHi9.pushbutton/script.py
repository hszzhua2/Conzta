import clr
import os
import winsound

# Load Revit API assemblies
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

class SampleCommand(IExternalCommand):
    def Execute(self, commandData):
        # Get the Revit application and document
        app = commandData.Application
        doc = app.ActiveUIDocument.Document
        
        # Define the push button data
        push_button_data = Revit.UI.PushButtonData("play_sound_button", "Play Sound", 
                                                    os.path.abspath(r"C:\Users\zhuangzefeng\Downloads\BeautifulChick.mp3"))
        
        # Add the push button to the Revit ribbon
        push_button = Revit.UI.RibbonItemFactory.CreatePushButton(push_button_data)

        
        return Result.Succeeded
    
    def play_sound(self, sender, args):
        # Play the MP3 file
        winsound.PlaySound(args.GetExecutionFilePath(), winsound.SND_FILENAME)

print("Done!")