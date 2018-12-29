#-*- utf-8 -*-
"""
list 的相关工具
"""

#arr是被分割的list，n是每个chunk中含n元素。
def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]

#或者让一共有m块，自动分（尽可能平均）
#split the arr into N chunks
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]