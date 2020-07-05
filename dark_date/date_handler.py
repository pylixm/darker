#-*- coding:utf-8 -*-
"""
common tools by corner
"""

def seconds_to_str( s ):
    """秒转化天 时 分 秒"""
    day = s / 86400
    hour = ( s % 86400 ) / 3600
    minute = ( s % 3600 ) / 60
    secs  = ( s % 60 )
    ret = ''
    if day:
        ret += '%d天' % day
    if hour:
        ret += '%d小时' % hour
    if minute:
        ret += '%d分' % minute
    if secs:
        ret += '%d秒' % secs
    return ret
    
    
if __name__=='__main__':
    print seconds_to_str( 8889182 )