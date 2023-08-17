import os, sys, stat
from tkinter import filedialog, messagebox

# 获取当前工作目录
dirPath = os.getcwd()

# 使用文件对话框选择Revit文件
filePaths = filedialog.askopenfilename(multiple=True,
                                       filetypes=[("Revit Families", ".rfa"), ("Revit Projects", ".rvt")],
                                       initialdir=dirPath)

# 函数用于提取Revit文件的版本信息
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

# 如果选择了文件
if filePaths:
    msgs = []

    # 遍历选中的文件并提取版本信息
    for fp in filePaths:
        fn = fp.rsplit("/", 1)[-1]
        if len(fn) > 40:
            fn = fn[39] + "..."
        ver = revitVersion(fp)[7:11]
        msg = fn + " (" + ver + ")"
        msgs.append(msg)

    # 将版本信息整合成一个消息字符串
    joinedMsg = "\n".join(msgs)

    # 在消息框中显示Revit文件的版本信息
    messagebox.showinfo("Revit文件格式", joinedMsg)
