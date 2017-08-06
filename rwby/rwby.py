#! /usr/bin/env python
################################################################################
#     File Name           :     draw.py
#     Created By          :     totorikira
#     Creation Date       :     [2017-07-31 17:37]
#     Last Modified       :     [2017-08-05 10:35]
#     Description         :     TotoriKira 的画画小工具
################################################################################


import os
from scipy import ndimage
import re
import time
import json
from urllib import request
import threading
import queue

# 画笔颜色信息
color = {
    '0': (0, 0, 0),
    '1': (255, 255, 255),
    '2': (252, 222, 107),
    '3': (255, 246, 209),
    '4': (125, 149, 145),
    '5': (113, 190, 214),
    '6': (59, 229, 219),
    '7': (254, 211, 199),
    '8': (184, 63, 39),
    '9': (250, 172, 142),
    'A': (0, 70, 112),
    'B': (5, 113, 151),
    'C': (68, 201, 95),
    'D': (119, 84, 255),
    'E': (255, 0, 0),
    'F': (255, 152, 0),
    'G': (151, 253, 220),
    'H': (248, 203, 140),
    'I': (46, 143, 175)
}

# Get gif map info
im_array = ndimage.imread("rwby.bmp", mode="RGB")
len_row = len(im_array)
len_col = len(im_array[0])

print(len_row, len_col)


# 基础绘画基准
base_row, base_col = 381, 1

# 画笔 请手工修改颜色对应信息，注意逗号之后的空格
# 数据按json格式输入，注意最后一行没有逗号
brush = \
    '''
{
    "(184, 63, 39)":"8",
    "(250, 172, 142)":"9",
    "(0, 0, 0)":"0",
    "(254, 211, 199)":"7",
    "(255, 255, 255)":"1",
    "(252, 222, 107)":"2",
    "(255, 0, 0)":"E"
}
'''
brush = (json.loads(brush))

# 线程同步用，pos记录要绘制区域，queue应该是线程安全的
pos = None

RefreshQueue = False

def getCMD(cURL):
    '''
        得到并利用正则表达式修改cURL
    '''

    pattern = re.compile(
        r'x_min=[0-9]+&y_min=[0-9]+&x_max=[0-9]+&y_max=[0-9]+&color=[0-9]+')
    request = pattern.sub(
        r"x_min={1}&y_min={0}&x_max={1}&y_max={0}&color={2}", cURL)
    # 此处x代表列，y代表行，format数据按 行，列，颜色 顺序输入
    request += '  --silent'  # 禁止系统curl函数回显

    return request


def getdiff(row, col):
    '''
        获得当前图片与目标图片的不同之处

        ret存储(x，y，目标颜色值)
    '''
    ret = []

    # 读取目标区域颜色分布
    while True:
        try:
            web = request.urlopen(
                "http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap")
            data = web.read().decode("utf-8")
            data = json.loads(data)['data']['bitmap']
            break
        except Exception as e:
            continue

    # 检查目标区域颜色与本区域的不同
    for i in range(row, row + len_row):
        for j in range(col, col + len_col):
            #  if brush[str(tuple(im_array[i - row][j - col]))] == '0':
            #      continue

            if brush[str(tuple(im_array[i - row][j - col]))] != data[i * 1280 + j]:
                ret.append((i, j, im_array[i - row][j - col]))

    return ret


def drawing(request):
    global pos, RefreshQueue

    while not RefreshQueue:
        try:
            i, j, k = pos.get(False)
            print("\t绘图位置：{0}  {1}".format(i, j))
            print("\t颜色信息(RGB)：", k)
            print("\t对应画笔信息：", brush[str(tuple(k))])
            while True:
                # popen
                try:
                    ret = os.popen(request.format(
                        i, j, brush[str(tuple(k))])).readlines()[0]
                except Exception as e:
                    continue

                print("\t网络请求返回值：", ret)
                ret = json.loads(ret)
                if ret['code'] == 0:
                    break
                elif ret['code'] == -400:
                    time.sleep(int(ret['data']['time']))
                else:
                    print("\t出错啦，进入下一次循环")

        except queue.Empty as e:
            print("\t队列为空，等待中")
            time.sleep(30)

    return


def watchDiff():
    return


def main():
    '''
        Daemon Threading
    '''
    global pos, RefreshQueue

    threads = []
    while True:
        # kill all Thread
        RefreshQueue = True
        print("等待所有子线程退出")
        for i in threads:
            i.join()
        threads = []
        print("子线程全部结束")

        # prepare pos queue
        pos = queue.Queue()

        ret = getdiff(base_row, base_col)

        if len(ret)==0:
            print("没有发现被污染的像素点，休眠中")
            time.sleep(60)
            continue

        print("发现被污染的像素点，正在处理中")

        for i in ret:
            pos.put(i)

        RefreshQueue = False
        # End of prepare pos queue

        # create Thread
        with open("cURLs.txt") as file:
            for i in file.readlines():
                tmp = threading.Thread(target=drawing, args=(getCMD(i[:-1]),))
                tmp.start()
                threads.append(tmp)

        print("进入长时间等待状态，剩余时间：%d" % min(len(ret)*180, 180*10))
        time.sleep(min(len(ret)*180//len(threads), 180*10))

    return


if __name__ == "__main__":
    main()
