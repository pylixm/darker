#coding: gbk
"""
读取excel文件中的数据
"""
import datetime
from pyExcelerator import *

def get_value( sheet_value ):
#取excel单元格中的数据
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
                ##非法字符的剔除操作。。。。
                illegl = sheet_value[ e[2] :e[3] ] 
                sheet_value = sheet_value.replace( illegl , '' )
    return sheet_value.strip()

def get_rowdata( sheetcontent, rows_begin, col_begin, col_end):
#获取Excel中的一行数据
    """
    @param:sheetcontent     #sheet中数据
    @param:rows_begin       #行号
    @param:col_begin        #列开始号
    @param:col_end          #列结束号
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

#获取一列数据
def get_coldata( sheetcontent  ,cols_begin  ,  row_begin , row_end):
    """
    @param:sheetcontent     #
    @param:cols_begin       #列号
    @param:row_begin        #行开始号
    @param:row_end          #行结束号
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
    #获取Excle中每个sheet页的名字
    sheets = parse_xls( fn_path )#打开excel文件
    sheets_len = len( sheets )
    return sheets,sheets_len

    
#def read_file( sheets,sheets_num,logf_path,cur, logInfo_list ):
#    #读取Excel数据文件，存储到字典中
#    sheet_name = sheets[sheets_num][0]
#    sheetcontent = sheets[ sheets_num ][1] # 字典
#    sheetname_list = [u'储蓄', u'对公', u'个人贷款']
#    if sheet_name in sheetname_list:
#        if sheetcontent:#判断此sheet页中是否有数据
#            if sheetcontent.has_key( (0,0) ):
#                try:
#                    ksyf = str( int( sheetcontent[(0,0)] ) )#开始月份
#                except:
#                    return sheet_name,'yf','',[],{}
#            else:
#                ksyf = ''
#            if sheetcontent.has_key( (0,1) ):
#                try:
#                    jsyf = str( int( sheetcontent[(0,1)] ) )#结束月份
#                except:
#                    return sheet_name,'yf','',[],{}
#            else:
#                jsyf = ''
#            """
#            若其中的一个月份为空，则把不为空月份的值赋给为空的月份的值，
#            若两个月份的值都为空，则把gl_xtcs中的当前月份赋值给两个月份
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
#            if ksyf.isdigit() and jsyf.isdigit():#开始月份和结束月份中的数据是否只包含数字
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
#                if zh_str == u'账号' and lcrbh_str == u'揽存人编号' and zb_str == u'占比':
#                    cols_begin = 0          #字段开始位置
#                    cols_end = 3            #字段结束位置
#                    rows_begin = 2          #数据开始行
#                    plfpdic = {}            #存储Excel中所有的数据
#                    lcrbhlist = []          #存储所有的揽存人
#                    zhlist = []             #存储所有的账号
#                    for row_data , rowno in get_rowdata( sheetcontent , rows_begin   ,  cols_begin , cols_end ):#一行一行的取数据
#                        zh = get_value( row_data[0])#获取账户数据
#                        try:#揽存人编号、占比数据格式不是数字时，捕获异常
#                            lcrbh = str(int( float( get_value( row_data[1]) )) ).rjust(6,'0')
#                            zb = int( float ( get_value( row_data[2] ) ) )
#                            if lcrbh not in lcrbhlist:              #如果揽存人list中无此账号，追加
#                                lcrbhlist.append( lcrbh )
#                            if zh not in zhlist:
#                                zhlist.append( zh )
#                            #存储格式{ zh: { lcrbh1:zb,lcrbh2:zb } }
#                            if plfpdic.has_key( zh ):
#                                if plfpdic[zh].has_key( lcrbh ):
#                                    plfpdic[zh][lcrbh] =  plfpdic[zh][lcrbh] + zb
#                                else:
#                                    plfpdic[zh][lcrbh] = zb
#                            else:
#                                plfpdic[zh] = { lcrbh:zb }
#                        except:
#                            msg = sheet_name + u"页中第"+ str(rowno) +u"行揽存人或者占比数据必须只包含数字数据，请校正！\n"
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