#! /usr/bin/env python
################################################################################
#     File Name           :     test.py
#     Created By          :     totorikira
#     Creation Date       :     [2017-08-04 15:39]
#     Last Modified       :     [2017-08-04 15:43]
#     Description         :
################################################################################

import json
from urllib import request

brush = \
    '''
{
    "(184, 63, 39)":"8",
    "(250, 172, 142)":"9",
    "(0, 0, 0)":"0",
    "(254, 211, 199)":"7",
    "(255, 255, 255)":"1"
}
'''

ret = json.loads(brush)
print(ret)


web = request.urlopen(
    "http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap")
data = web.read().decode("utf-8")
data = json.loads(data)['data']['bitmap']

print(repr(data[ 399*1280+315 ]))
