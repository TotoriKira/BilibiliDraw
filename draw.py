#! /usr/bin/env python
################################################################################
#     File Name           :     draw.py
#     Created By          :     totorikira
#     Creation Date       :     [2017-07-31 17:37]
#     Last Modified       :     [2017-08-04 01:03]
#     Description         :     TotoriKira 的画画小工具
################################################################################


import os
from scipy import ndimage
import re
import time
import json
from urllib import request

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
    'I': (46, 143, 175),
}

# Get gif map info
im_array = ndimage.imread("ref.png", mode="RGB")
len_row = len(im_array)
len_col = len(im_array[0])

print(len_row, len_col)


def getCMD():
    '''
        得到并利用正则表达式修改cURL
    '''

    print("\n请输入cURL（可从Chrome F12控制台得到）:")
    cURL = input()

    pattern = re.compile(
        r'x_min=[0-9]+&y_min=[0-9]+&x_max=[0-9]+&y_max=[0-9]+&color=[0-9]+')
    request = pattern.sub(
        r"x_min={1}&y_min={0}&x_max={1}&y_max={0}&color={2}", cURL)
    # 此处x代表列，y代表行，format数据按 行，列，颜色 顺序输入
    request += '  --silent' # 禁止系统curl函数回显

    return request


def getdiff(row, col):
    '''
        获得当前图片与目标图片的不同之处

        ret存储(x，y，目标颜色值)
    '''
    ret = []

    # 读取目标区域颜色分布
    web = request.urlopen(
        "http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap")
    data = web.read().decode("utf-8")
    data = json.loads(data)['data']['bitmap']

    # 检查目标区域颜色与本区域的不同
    for i in range(row, row + len_row):
        for j in range(col, col + len_col):
            if im_array[i - row][j - col] != data[i * 1280 + j]:
                ret.append((i, j, im_array[i - row][j - col]))

    return ret


def main():
    '''
        主函数
    '''

    # 基础绘画基准
    base_row, base_col = 381, 0

    # 画笔 请手工修改颜色对应信息，注意逗号之后的空格
    # 数据按json格式输入，注意最后一行没有逗号
    brush = \
        '''
        {
            "(0, 0, 0)":"E",
            "(255, 255, 255)":"G"
        }
    '''
    brush = (json.loads(brush))

    # Start output process
    request = getCMD()

    while True:
        diff = getdiff(base_row, base_col)

        for i, j, k in diff:
            print("绘图位置：{0}  {1}".format(i, j))
            print("颜色信息(RGB)：", k)
            print("对应画笔信息：", brush[str(tuple(k))])
            while True:
                # popen
                ret = os.popen(request.format(
                    i, j, brush[str(tuple(k))])).readlines()[0]

                print("网络请求返回值：", ret)
                ret = json.loads(ret)
                if ret['code'] == 0:
                    break
                elif ret['code'] == -400:
                    time.sleep(int(ret['data']['time']))
                else:
                    # 存在因为心跳数据的缘故而要求重新登录的情况
                    # 建议一直开着浏览器返回心跳数据
                    # 其实就是我懒得写了
                    print("Something is Wrong")
                    request = getCMD()

    return


if __name__ == "__main__":
    main()
