#coding:gbk
"""
    读取不同编码集类型的文件
"""

from shangjie.conf import settings
import os
from datetime import datetime
from const import zf_type
try:
    import uuid
except:
    import fake_uuid as uuid

# 将文件内容保存在服务器上
def upload2host(file_prefix ,file_obj):
    """
        @param:file_prefix:文件前缀
        @param:file_obj: req.FILES.get( 'questioninfo', None )
        返回值：服务器 文件路径+文件名
    """
    file_type = file_obj.get('filename' , '*.yaml').split('.')[-1].lower()       #文件类型
    fname = '%s_%s_%s.%s' % (file_prefix ,datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() ,file_type)   # 导入数据文件的文件名
    fn = os.path.join( settings.FILE_TEMP, fname )
    fi = file( fn, 'wb' )
    fi.write( file_obj[ 'content' ] )
    fi.close()
    return (fn ,fname)

# 从文件中读取数据
def inputTXT(filestr):
    """
        @param:filestr:文件路径
        返回值：[(hh,line),(hh,line),...]
    """
    lines_list = [] # 文件的内容
    decode_type = ''#decode转换类型
    file_nr = ''    #文件内容
    try:
        #UTF-16 le, UTF-16 be, UTF-8, gbk
        ##首先检查 utf-16
        f = file( filestr , 'rb' )
        type_2 = f.read( 2 )
        decode_type = zf_type.get( type_2, '' )
        if decode_type == '': ##检查utf-8
            f = file( filestr , 'rb' )
            type_3 = f.read( 3 )
            decode_type = zf_type.get( type_3, '' )
        if decode_type == '': ##不是uft-16、utf-8,则认为是gbk
            f = file( filestr , 'rb' )
            file_nr = f.read().decode('gbk').encode('gbk')
        else:
            nr = f.read()
            nr = nr.decode( decode_type )
            file_nr = nr.encode( 'gbk' )
        #处理文件内容
        i = 0
        for line in file_nr.split( '\n' ):  # 读取文件内容，添加行号
            i += 1 # 行号
            if line.strip():
                lines_list.append( ( i , line.strip().replace( '，', ',' ) ) )
        f.close()
    except:
        lines_list.append( ( 0,'文件编码集未知，不能正确导入文件，请联系科技部人员；本系统支持utf-16 le, utf-16 be, utf-8, gbk2312四种编码集') )
    return lines_list
    
# 将错误信息写入TXT文件
def outtoTXT(listlines):
    """
        @param listlines : [(行号，内容，错误信息),(行号，内容，错误信息)]
    """
    filename='error_%s_%s.txt'% ( datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() )
    path = os.path.join( settings.FILE_TEMP , filename )##将文件写到了服务器的temp目录下，为避免重复，取文件名时，应取不同的名字，可以用uuid
    file_new = open( path, 'w' ) # 新文件
    for hh, line ,errorstr in listlines:
        if hh == 0:
            str_new = "%s\n" % ( errorstr )
        else:
            str_new = "第%4s 行        %s        %s\n" % ( hh, line ,errorstr )
        file_new.write( str_new )
    file_new.close()
    return filename

# 将错误信息写入TXT文件
def write_errfile( err_nrdic ):
    """
        @param err_nrdic : 所有的数据记录 {行号:(内容，错误信息),行号:(内容，错误信息)}
    """
    filename='error_%s_%s.txt'% ( datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() )
    path = os.path.join( settings.FILE_TEMP , filename )##将文件写到了服务器的temp目录下，为避免重复，取文件名时，应取不同的名字，可以用uuid
    file_new = open( path, 'w' ) # 新文件
    line_lst = sorted( err_nrdic.keys() )
    for k in line_lst:
        str_new = ""
        if k == 0:
            str_new = err_nrdic.get(k)[1]
        else:
            str_new = "第 %s 行\t\t%s\t\t%s\n" % ( k, err_nrdic.get(k)[0] ,err_nrdic.get(k)[1] )
        file_new.write( str_new )
    file_new.close()
    return filename

# 过滤重复数据
def filterlines(listlines):
    """
        @param listlines : 所有的数据记录 [(行号，内容)]
    """
    list_ok = [] # 过滤后的数据
    list_only = [] # 用于识别数据是否唯一
    for hh, line in listlines:
        if line not in list_only:
            list_only.append( line )
            list_ok.append( (hh ,line) )
    return list_ok
