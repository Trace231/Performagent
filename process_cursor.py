#!/usr/bin/env python3
"""处理 true.jpeg：水平镜像、去背景、输出透明 PNG 作为鼠标光标。"""
from PIL import Image
import os

def is_bg(r, g, b):
    target = (248, 242, 247)  # #F8F2F7
    return all(abs(c - t) < 35 for c, t in zip((r, g, b), target))

path = os.path.join(os.path.dirname(__file__), 'true.jpeg')
out_path = os.path.join(os.path.dirname(__file__), 'cursor.png')

img = Image.open(path).convert('RGBA')
img = img.transpose(Image.FLIP_LEFT_RIGHT)

w, h = img.size
data = img.getdata()
out = []
for i, (r, g, b, a) in enumerate(data):
    if is_bg(r, g, b):
        out.append((r, g, b, 0))
    else:
        out.append((r, g, b, a))

img.putdata(out)
img = img.resize((48, 48), Image.Resampling.LANCZOS)
img.save(out_path, 'PNG')
print('Saved:', out_path)

# 按下态：缩小至 90%，营造按压感
pressed = img.resize((43, 43), Image.Resampling.LANCZOS)
padded = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
padded.paste(pressed, (2, 2))
pressed_path = os.path.join(os.path.dirname(__file__), 'cursor-pressed.png')
padded.save(pressed_path, 'PNG')
print('Saved:', pressed_path)
