#-*- utf-8 -*-
"""
list 操作
"""
import math

def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]

#split the arr into N chunks
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]