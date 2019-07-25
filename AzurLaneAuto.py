# -*- coding: utf-8 -*-
import cv2
import os
import random
import sys
import time
from PIL import Image
import Moving
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

adb = auto_adb()
adb.test_device()


def tap_scale(pos, scale):
    scaled_pos = int(pos[0] * scale[0]), int(pos[1] * scale[1])
    print(scaled_pos)
    adb.run('shell input tap {} {}'.format(scaled_pos[0], scaled_pos[1]))
    return scaled_pos


def main():
    screenshot.check_screenshot()
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    x, y = adb.get_size()
    if x < y:
        x, y = y, x
    scale = (x / 960, y / 443)
    pos, val = Moving.find_stage(im, '3-4')
    tap_scale(pos, scale)
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    pos, val = Moving.go(im)
    tap_scale(pos, scale)
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    pos, val = Moving.go(im)
    tap_scale(pos, scale)
    time.sleep(4)
    while True:
        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        pos = Moving.find_enemy(im)
        posx = pos
        tap_scale(pos, scale)
        time.sleep(4.5)
        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        pos, val = Moving.attack(im)
        if val < 0.05:
            print('出击！')
            tap_scale(pos, scale)
        else:
            pos, val = Moving.ambush(im)
            if val < 0.1:
                print('遭遇伏击！规避')
                pos, val = Moving.escape(im)
                tap_scale(pos, scale)
            else:
                print('遭遇空袭！继续进行')
                tap_scale(posx, scale)
            # 继续
            tap_scale(posx, scale)
            time.sleep(2.5)
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.attack(im)
            # 出击
            tap_scale(pos, scale)
        val = 1
        while val > 0.06:
            print("判断是否战斗结束，若未能进入战斗状态，请手动进入战斗")
            time.sleep(1)
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.finished(im)
        tap_scale(pos, scale)
        time.sleep(0.5)
        tap_scale((500, 300), scale)
        time.sleep(1.5)
        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        pos, val = Moving.accept(im)
        tap_scale(pos, scale)
        time.sleep(4.5)
        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        pos, val = Moving.find_stage(im, '3-4')
        if val < 0.06:
            tap_scale(pos, scale)
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.go(im)
            tap_scale(pos, scale)
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.go(im)
            tap_scale(pos, scale)
            time.sleep(4)


if __name__ == '__main__':
    main()
