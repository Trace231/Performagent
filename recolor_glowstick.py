#!/usr/bin/env python3
"""
处理 未命名.png 荧光棒素材：
1. 去除棕色背景（变透明）
2. 星星填金黄色、灯体填紫色、柄填搭配色
"""
from PIL import Image
import os
from collections import deque

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '未命名.png')
OUT = os.path.join(BASE, '荧光棒.png')

# 颜色定义
GOLDEN_YELLOW = (255, 200, 50, 255)   # 星星 金黄色
PURPLE       = (160, 100, 220, 255)   # 灯体 紫色
HANDLE       = (100, 80, 160, 255)   # 柄 深紫/灰紫 与灯体搭配

def is_brown(r, g, b, a, tol=25):
    """背景棕 #494539 约 (73,66,53)"""
    return (a == 255 and 45 <= r <= 95 and 45 <= g <= 90 and 40 <= b <= 70
            and abs(r - g) < 25 and abs(g - b) < 25)

def get_transparent_components(w, h, alpha_channel):
    """对透明像素做连通分量，返回各分量像素集合（不含贴边的 exterior）。"""
    visited = set()
    components = []
    for y in range(h):
        for x in range(w):
            if alpha_channel[y * w + x] != 0:
                continue
            if (x, y) in visited:
                continue
            # BFS
            comp = set()
            q = deque([(x, y)])
            visited.add((x, y))
            touches_border = False
            while q:
                cx, cy = q.popleft()
                comp.add((cx, cy))
                if cx == 0 or cy == 0 or cx == w - 1 or cy == h - 1:
                    touches_border = True
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                        if alpha_channel[ny * w + nx] == 0:
                            visited.add((nx, ny))
                            q.append((nx, ny))
            if not touches_border and len(comp) > 20:  # 忽略太小的噪点
                components.append(comp)
    return components

def main():
    img = Image.open(SRC).convert('RGBA')
    w, h = img.size
    data = list(img.getdata())
    out = [list(p) for p in data]

    # 1. 棕色背景变透明
    for i, (r, g, b, a) in enumerate(data):
        if is_brown(r, g, b, a):
            out[i] = [0, 0, 0, 0]

    # 重建 alpha 通道供后续用
    alpha = [out[i][3] for i in range(w * h)]
    # 2. 找封闭透明区域（黑线内部的“洞”）
    components = get_transparent_components(w, h, alpha)
    if not components:
        img.putdata([tuple(p) for p in out])
        img.save(OUT, 'PNG')
        print('No interior regions found, only background removed. Saved:', OUT)
        return

    # 按面积、重心分类：两颗星（小）、灯体（大且偏上中）、柄（偏下左）
    def info(c):
        xs = [x for x, y in c]
        ys = [y for x, y in c]
        cx = sum(xs) / len(c)
        cy = sum(ys) / len(c)
        return len(c), cy, cx

    comps_sorted = sorted(components, key=info)
    # 面积从小到大：通常两颗星最小，柄次之，灯体最大
    by_area = comps_sorted
    n = len(by_area)
    stars = []
    body = None
    handle = None
    if n >= 4:
        # 两个最小的多为星星
        stars = [by_area[0], by_area[1]]
        # 最大的多为灯体，其次为柄（柄在下方）
        by_cy = sorted(by_area[2:], key=lambda c: sum(y for _, y in c) / len(c))
        handle = by_cy[0]   # 更靠下
        body = by_cy[1]
    elif n == 3:
        by_cy = sorted(by_area, key=lambda c: sum(y for _, y in c) / len(c))
        stars = [by_cy[0]] if len(by_cy[0]) < min(len(by_cy[1]), len(by_cy[2])) else []
        if len(stars) == 1:
            rest = [c for c in by_area if c not in stars]
            if len(rest) == 2:
                by_cy_rest = sorted(rest, key=lambda c: sum(y for _, y in c) / len(c))
                handle, body = by_cy_rest[0], by_cy_rest[1]
        else:
            handle, body = by_cy[0], by_cy[1]
            if len(by_cy) > 2:
                stars = [by_cy[2]] if len(by_cy[2]) < 500 else []
    else:
        body = by_area[-1]
        if n >= 2:
            handle = by_area[0]

    def fill_comp(pixels, color):
        for (px, py) in pixels:
            idx = py * w + px
            out[idx] = [color[0], color[1], color[2], color[3]]

    for c in stars:
        fill_comp(c, GOLDEN_YELLOW)
    if body:
        fill_comp(body, PURPLE)
    if handle:
        fill_comp(handle, HANDLE)

    img.putdata([tuple(p) for p in out])
    img.save(OUT, 'PNG')
    print('Saved:', OUT)

if __name__ == '__main__':
    main()
