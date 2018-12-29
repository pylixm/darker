#coding: gbk
"""
��ȡexcel�ļ��е�����
"""
import datetime
from pyExcelerator import *

def get_value( sheet_value ):
#ȡexcel��Ԫ���е�����
    if isinstance( sheet_value, float ):
        sheet_value = str( float( sheet_value ) )
    elif isinstance( sheet_value, int ):
        sheet_value = str( sheet_value )
    elif isinstance( sheet_value, long ):
        sheet_value = str( sheet_value )
    else:
        while True:
            try:
                sheet_value = sheet_value.encode( 'gbk' )
                break
            except Exception , e:
                ##�Ƿ��ַ����޳�������������
                illegl = sheet_value[ e[2] :e[3] ] 
                sheet_value = sheet_value.replace( illegl , '' )
    return sheet_value.strip()

def get_rowdata( sheetcontent, rows_begin, col_begin, col_end):
#��ȡExcel�е�һ������
    """
    @param:sheetcontent     #sheet������
    @param:rows_begin       #�к�
    @param:col_begin        #�п�ʼ��
    @param:col_end          #�н�����
    """
    cols = []
    for c in range( col_begin , col_end+1 ):
        cols.append(c)
    sortedkeys = sheetcontent.keys()
    rows = list( set( map(lambda x:x[0] , sortedkeys) ) )
    rows.sort() 
    for rowno in range(rows_begin):
        if rowno in rows:
            rows.remove( rowno )
    for  i in rows:
        row_data = map(lambda x:sheetcontent.get((i , x),'') , cols)
        yield row_data , i

#��ȡһ������
def get_coldata( sheetcontent  ,cols_begin  ,  row_begin , row_end):
    """
    @param:sheetcontent     #
    @param:cols_begin       #�к�
    @param:row_begin        #�п�ʼ��
    @param:row_end          #�н�����
    """
    rows = []
    for c in range( row_begin , row_end+1 ):
        rows.append(c)
    sortedkeys = sheetcontent.keys()
    cols = list( set( map(lambda x:x[1] , sortedkeys) ) )
    cols.sort() 
    for colno in range(cols_begin):
        cols.remove( colno )
    for  i in cols:
        col_data = map(lambda x:sheetcontent.get((x , i),'') , rows)
        yield col_data , i

def get_sheet( fn_path ):
    #��ȡExcle��ÿ��sheetҳ������
    sheets = parse_xls( fn_path )#��excel�ļ�
    sheets_len = len( sheets )
    return sheets,sheets_len

    
#def read_file( sheets,sheets_num,logf_path,cur, logInfo_list ):
#    #��ȡExcel�����ļ����洢���ֵ���
#    sheet_name = sheets[sheets_num][0]
#    sheetcontent = sheets[ sheets_num ][1] # �ֵ�
#    sheetname_list = [u'����', u'�Թ�', u'���˴���']
#    if sheet_name in sheetname_list:
#        if sheetcontent:#�жϴ�sheetҳ���Ƿ�������
#            if sheetcontent.has_key( (0,0) ):
#                try:
#                    ksyf = str( int( sheetcontent[(0,0)] ) )#��ʼ�·�
#                except:
#                    return sheet_name,'yf','',[],{}
#            else:
#                ksyf = ''
#            if sheetcontent.has_key( (0,1) ):
#                try:
#                    jsyf = str( int( sheetcontent[(0,1)] ) )#�����·�
#                except:
#                    return sheet_name,'yf','',[],{}
#            else:
#                jsyf = ''
#            """
#            �����е�һ���·�Ϊ�գ���Ѳ�Ϊ���·ݵ�ֵ����Ϊ�յ��·ݵ�ֵ��
#            �������·ݵ�ֵ��Ϊ�գ����gl_xtcs�еĵ�ǰ�·ݸ�ֵ�������·�
#            """
#            if ksyf == '' and jsyf != '':
#                ksyf = jsyf
#            if ksyf != '' and jsyf == '':
#                jsyf = ksyf
#            if ksyf == '' and jsyf == '':
#                sql = """ select substr(csqz3,1,6) from gl_xtcs where csdm = 'rhz'  """
#                cur.execute( sql )
#                ksyf = cur.fetchone()[0]
#                jsyf = ksyf
#            
#            if ksyf.isdigit() and jsyf.isdigit():#��ʼ�·ݺͽ����·��е������Ƿ�ֻ��������
#                if sheetcontent.has_key( (1,0) ):
#                    zh_str = sheetcontent[(1,0)]
#                else:
#                    zh_str = ''
#                if sheetcontent.has_key( (1,1) ):
#                    lcrbh_str = sheetcontent[(1,1)]
#                else:
#                    lcrbh_str = ''
#                if sheetcontent.has_key( (1,2) ):
#                    zb_str = sheetcontent[(1,2)]
#                else:
#                    zb_str = ''
#                if zh_str == u'�˺�' and lcrbh_str == u'�����˱��' and zb_str == u'ռ��':
#                    cols_begin = 0          #�ֶο�ʼλ��
#                    cols_end = 3            #�ֶν���λ��
#                    rows_begin = 2          #���ݿ�ʼ��
#                    plfpdic = {}            #�洢Excel�����е�����
#                    lcrbhlist = []          #�洢���е�������
#                    zhlist = []             #�洢���е��˺�
#                    for row_data , rowno in get_rowdata( sheetcontent , rows_begin   ,  cols_begin , cols_end ):#һ��һ�е�ȡ����
#                        zh = get_value( row_data[0])#��ȡ�˻�����
#                        try:#�����˱�š�ռ�����ݸ�ʽ��������ʱ�������쳣
#                            lcrbh = str(int( float( get_value( row_data[1]) )) ).rjust(6,'0')
#                            zb = int( float ( get_value( row_data[2] ) ) )
#                            if lcrbh not in lcrbhlist:              #���������list���޴��˺ţ�׷��
#                                lcrbhlist.append( lcrbh )
#                            if zh not in zhlist:
#                                zhlist.append( zh )
#                            #�洢��ʽ{ zh: { lcrbh1:zb,lcrbh2:zb } }
#                            if plfpdic.has_key( zh ):
#                                if plfpdic[zh].has_key( lcrbh ):
#                                    plfpdic[zh][lcrbh] =  plfpdic[zh][lcrbh] + zb
#                                else:
#                                    plfpdic[zh][lcrbh] = zb
#                            else:
#                                plfpdic[zh] = { lcrbh:zb }
#                        except:
#                            msg = sheet_name + u"ҳ�е�"+ str(rowno) +u"�������˻���ռ�����ݱ���ֻ�����������ݣ���У����\n"
#                            logInfo_list.append(msg)
#                    return sheet_name, ksyf, jsyf, lcrbhlist, plfpdic
#                else:
#                    return sheet_name,'bt','',[],{}
#            else:
#                return sheet_name,'yf','',[],{}
#        else:
#            return sheet_name,'','',[],{}
#    else:
#        return sheet_name,'sheet_name','',[],{}