from pyrevit import revit, DB, script, forms

dirPath = forms.pick_folder(title = "Choose a directory please.")

if not dirPath: 
    script.exit()

#choose a run mode
sub = "Choose carefully, large directories can take a while..."
msg = "Would you like to read sub-directoried as well as the root level?"

runMode = forms.alert(msg, sub_msg = sub, title = "Choose run mode", ok=False, yes=True, no=True, warn_icon=False)

if runMode == None:
    script.exit()

#libraries for searching
import clr 
from System.IO import Directory, SearchOption

#make function to get file
def directory_getFamilies(dirPath, deepSearch = False):
    filePaths, fileNames = [], []
    if Directory.Exists(dirPath):
        if deepSearch:
            mode = SearchOption.AllDirectories
        else:
            mode = SearchOption.TopDirectoryOnly
            dirPaths = Directory.GetFiles(filePaths, ".", mode)
            #Get family files only
            for fp in dirPaths:
                if ".rfa" in fp:
                    if ".00" not in fp:
                        filePaths.append(fp)
                        #get file name
                        fileName = fp.rsplit("\\", 1)[-1]
                        noExt    = fileName.replace(".rfa", "")
                        fileNames.append(noExt)
    #return outcomes                    
    return [filePaths, fileNames]


#Get filr paths and names of family files
filePaths, fileNames = directory_getFamilies(dirPath, runMode)

if len(filePaths) == 0:
    forms.alert("No family found in directories.", title = "Script Cancelled.")
    script.exit()

print(fileNames)


