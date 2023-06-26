import os

mp3_file = r"C:\Users\zhuangzefeng\Downloads\aigei_com.mp3"
potplayer_exe = r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe"

if os.path.exists(mp3_file):
    os.system('"%s" "%s"' % (potplayer_exe, mp3_file))
else:
    print("Error!")