#! /usr/bin/env python
################################################################################
#     File Name           :     color.py
#     Created By          :     totorikira
#     Creation Date       :     [2017-07-31 20:55]
#     Last Modified       :     [2017-08-04 01:04]
#     Description         :     Get Color 2 Number
################################################################################

from scipy import ndimage


def main():
    '''
        获得全部颜色信息
    '''

    im_array = ndimage.imread("ref.png", mode='RGB')

    color = set()

    for i in im_array:
        for j in i:
            color.add(tuple(j))

    print('{')
    for i in color:
        print("\"{0}\":,".format(i))
    print('}')

    #  for noi,i in enumerate(im_array):
    #      for noj,j in enumerate(i):
    #          print("Row:%d Col:%d  color: %s" %(noi, noj, j))

if __name__ == "__main__":
    main()
