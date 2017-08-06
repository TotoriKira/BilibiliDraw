#! /usr/bin/env python
################################################################################
#     File Name           :     color.py
#     Created By          :     totorikira
#     Creation Date       :     [2017-07-31 20:55]
#     Last Modified       :     [2017-08-05 14:18]
#     Description         :     Get Color 2 Number
################################################################################

from scipy import ndimage
from scipy import misc
import numpy as np


def main():
    '''
        获得全部颜色信息
    '''

    im_array = ndimage.imread("greytech.png", mode='RGB')

    print(len(im_array), len(im_array[0]))

    color = set()

    for i in im_array:
        for j in i:
            color.add(tuple(j))

    #  tmp = [[0 for i in range(len(im_array[0]))] for j in range(len(im_array))]
    #
    #  for i in range((len(im_array))):
    #      for j in range(len(im_array[0])):
    #          print(str(tuple(im_array[i][j])))
    #          if str(tuple(im_array[i][j]))!= "(255, 255, 255)":
    #              tmp[i][j]=(0,0,0)
    #          else:
    #              tmp[i][j]=im_array[i][j]
    #
    #  misc.imsave("test.bmp", tmp)


    print('{')
    for i in color:
        print("\"{0}\":,".format(i))
    print('}')

    #  for noi,i in enumerate(im_array):
    #      for noj,j in enumerate(i):
    #          print("Row:%d Col:%d  color: %s" %(noi, noj, j))

if __name__ == "__main__":
    main()
