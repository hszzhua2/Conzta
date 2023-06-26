# -*- coding: utf-8 -*-
print("Loading...")
import pyrevit
import sys
sys.path.append(r"C:\Users\zhuangzefeng\AppData\Roaming\pyRevit-Master\site-packages")
try:
    
    print(sys.executable)
    print(sys.prefix)
    
except:
    print(".....Error!!")

time = pyrevit.coreutils.current_time()
date = pyrevit.coreutils.current_date()
print("现在时间是"+ time +","+ date)

