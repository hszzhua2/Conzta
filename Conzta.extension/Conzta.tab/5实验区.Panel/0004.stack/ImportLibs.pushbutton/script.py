from PIL import Image
import base64

# Open image file
with open("image.png", "rb") as img_file:
    # Read image content
    img_content = img_file.read(r'C:\Users\zhuangzefeng\Desktop\20190327172547_54242.png')


img_base64 = base64.b64encode(img_content).decode('utf-8')

print(img_base64)
