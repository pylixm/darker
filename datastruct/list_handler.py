#-*- utf-8 -*-
"""
list ����ع���
"""

#arr�Ǳ��ָ��list��n��ÿ��chunk�к�nԪ�ء�
def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]

#������һ����m�飬�Զ��֣�������ƽ����
#split the arr into N chunks
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]