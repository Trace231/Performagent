#!/usr/bin/env python3
"""去掉 荧光棒.jpeg 的浅色/棋盘格背景，输出透明 PNG。"""
from PIL import Image
import os

path = os.path.join(os.path.dirname(__file__), '荧光棒.jpeg')
out_path = os.path.join(os.path.dirname(__file__), '荧光棒.png')

img = Image.open(path).convert('RGBA')
w, h = img.size
data = img.getdata()
out = []
# 阈值：接近白或浅灰的像素视为背景变透明
# 棋盘格通常是 (255,255,255) 与 (190~210 的灰)
def is_bg(r, g, b):
    if r > 250 and g > 250 and b > 250:
        return True
    gray = (r + g + b) / 3
    if gray > 230:  # 很亮的都当背景
        return True
    # 浅灰棋盘格
    if 180 < gray < 245 and abs(r - g) < 25 and abs(g - b) < 25:
        return True
    return False

for i, (r, g, b, a) in enumerate(data):
    if is_bg(r, g, b):
        out.append((r, g, b, 0))
    else:
        out.append((r, g, b, a))

img.putdata(out)
img.save(out_path, 'PNG')
print('Saved:', out_path)
