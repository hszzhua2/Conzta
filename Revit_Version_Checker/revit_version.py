import os, sys, stat
from tkinter import filedialog, messagebox

dirPath = os.getcwd()
filePaths = filedialog.askopenfilename(multiple=True,
                                       filetypes=[("Revit Families", ".rfa"), ("Revit Projects", ".rvt")],
                                       initialdir=dirPath)


def revitVersion(filePath):
    file = open(filePath, 'rb')
    data = file.read()
    file.close()
    try:
        os.chmod(filePath, stat.S_IWRITE)
    except:
        pass
    s = 'Build'.encode('UTF-16-LE')
    i = data.find(s)
    if i > 0:
        build_string = data[i:i + 40]
        return build_string.decode('UTF-16-LE')
    else:
        return "Build: ??????_???"


if filePaths:

    msgs = []

    for fp in filePaths:
        fn = fp.rsplit("/", 1)[-1]
        if len(fn) > 40:
            fn = fn[39] + "..."
        ver = revitVersion(fp)[7:11]
        msg = fn + " (" + ver + ")"
        msgs.append(msg)

    joinedMsg = "\n".join(msgs)

    messagebox.showinfo ("Revit file formats", joinedMsg)
