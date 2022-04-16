from PIL import Image, ImageDraw
import os

img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标
# 第二个参数：表示写入内容
# 第三个参数：表示颜色
draw.text([0, 0], 'Django', "red")

with open(os.path.join(os.getcwd(), "TEMP", "code.png"), 'wb') as f:
    img.save(f, format='png')
