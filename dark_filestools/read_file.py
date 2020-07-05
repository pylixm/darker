#coding:gbk
"""
    ��ȡ��ͬ���뼯���͵��ļ�
"""

from shangjie.conf import settings
import os
from datetime import datetime
from const import zf_type
try:
    import uuid
except:
    import fake_uuid as uuid

# ���ļ����ݱ����ڷ�������
def upload2host(file_prefix ,file_obj):
    """
        @param:file_prefix:�ļ�ǰ׺
        @param:file_obj: req.FILES.get( 'questioninfo', None )
        ����ֵ�������� �ļ�·��+�ļ���
    """
    file_type = file_obj.get('filename' , '*.yaml').split('.')[-1].lower()       #�ļ�����
    fname = '%s_%s_%s.%s' % (file_prefix ,datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() ,file_type)   # ���������ļ����ļ���
    fn = os.path.join( settings.FILE_TEMP, fname )
    fi = file( fn, 'wb' )
    fi.write( file_obj[ 'content' ] )
    fi.close()
    return (fn ,fname)

# ���ļ��ж�ȡ����
def inputTXT(filestr):
    """
        @param:filestr:�ļ�·��
        ����ֵ��[(hh,line),(hh,line),...]
    """
    lines_list = [] # �ļ�������
    decode_type = ''#decodeת������
    file_nr = ''    #�ļ�����
    try:
        #UTF-16 le, UTF-16 be, UTF-8, gbk
        ##���ȼ�� utf-16
        f = file( filestr , 'rb' )
        type_2 = f.read( 2 )
        decode_type = zf_type.get( type_2, '' )
        if decode_type == '': ##���utf-8
            f = file( filestr , 'rb' )
            type_3 = f.read( 3 )
            decode_type = zf_type.get( type_3, '' )
        if decode_type == '': ##����uft-16��utf-8,����Ϊ��gbk
            f = file( filestr , 'rb' )
            file_nr = f.read().decode('gbk').encode('gbk')
        else:
            nr = f.read()
            nr = nr.decode( decode_type )
            file_nr = nr.encode( 'gbk' )
        #�����ļ�����
        i = 0
        for line in file_nr.split( '\n' ):  # ��ȡ�ļ����ݣ�����к�
            i += 1 # �к�
            if line.strip():
                lines_list.append( ( i , line.strip().replace( '��', ',' ) ) )
        f.close()
    except:
        lines_list.append( ( 0,'�ļ����뼯δ֪��������ȷ�����ļ�������ϵ�Ƽ�����Ա����ϵͳ֧��utf-16 le, utf-16 be, utf-8, gbk2312���ֱ��뼯') )
    return lines_list
    
# ��������Ϣд��TXT�ļ�
def outtoTXT(listlines):
    """
        @param listlines : [(�кţ����ݣ�������Ϣ),(�кţ����ݣ�������Ϣ)]
    """
    filename='error_%s_%s.txt'% ( datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() )
    path = os.path.join( settings.FILE_TEMP , filename )##���ļ�д���˷�������tempĿ¼�£�Ϊ�����ظ���ȡ�ļ���ʱ��Ӧȡ��ͬ�����֣�������uuid
    file_new = open( path, 'w' ) # ���ļ�
    for hh, line ,errorstr in listlines:
        if hh == 0:
            str_new = "%s\n" % ( errorstr )
        else:
            str_new = "��%4s ��        %s        %s\n" % ( hh, line ,errorstr )
        file_new.write( str_new )
    file_new.close()
    return filename

# ��������Ϣд��TXT�ļ�
def write_errfile( err_nrdic ):
    """
        @param err_nrdic : ���е����ݼ�¼ {�к�:(���ݣ�������Ϣ),�к�:(���ݣ�������Ϣ)}
    """
    filename='error_%s_%s.txt'% ( datetime.now().strftime( '%Y%m%d%H%M%S' ), uuid.uuid1().get_hex().lower() )
    path = os.path.join( settings.FILE_TEMP , filename )##���ļ�д���˷�������tempĿ¼�£�Ϊ�����ظ���ȡ�ļ���ʱ��Ӧȡ��ͬ�����֣�������uuid
    file_new = open( path, 'w' ) # ���ļ�
    line_lst = sorted( err_nrdic.keys() )
    for k in line_lst:
        str_new = ""
        if k == 0:
            str_new = err_nrdic.get(k)[1]
        else:
            str_new = "�� %s ��\t\t%s\t\t%s\n" % ( k, err_nrdic.get(k)[0] ,err_nrdic.get(k)[1] )
        file_new.write( str_new )
    file_new.close()
    return filename

# �����ظ�����
def filterlines(listlines):
    """
        @param listlines : ���е����ݼ�¼ [(�кţ�����)]
    """
    list_ok = [] # ���˺������
    list_only = [] # ����ʶ�������Ƿ�Ψһ
    for hh, line in listlines:
        if line not in list_only:
            list_only.append( line )
            list_ok.append( (hh ,line) )
    return list_ok
