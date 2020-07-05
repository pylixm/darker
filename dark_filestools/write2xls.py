# coding: gbk
"""
������򵥷�װpyExceleratorģ�飬ʵ����XLS�࣬�û���֪ͨ����ഴ��Excel����
����ʹ�÷�ʽ��
    1.����ʵ����myxls = XLS()
    2.д��ͷ��myxls.title( ['��Ա����', '��Ա����', '��������', '��������'] )
    3.д���壺myxls.content( [ ['0001', '����', '01', '�칫��'], ['0002', '����', '02', '�Ƽ���'], ] )
    4.���棺myxls.save( 'my.xls' )
���㣺
    1.��ʽ��һ��Ŀǰֻ��ȫ��Ĭ��Ϊ�б߿�û�����������κ���ʽ
    2.�޹�ʽ�û�д������ۼӡ�����ƽ�����ȹ�ʽ��Ľӿ�
    3.��ʽ��һ������ȫ��Ϊ�ַ������޷�ͨ����ק�ۼ����
    4.��ͷ������û��ͳһ�޶���Ŀǰ�����ͷ��������岻��Ӧ
"""
from pyExcelerator import *
import os 
from django.http import HttpResponseRedirect, HttpResponse
from shangjie.conf import settings

class XLS:
    def __init__( self, sheet = 'Sheet1', border_style = 1 ):
        # ����Excel�����û�ָ��sheet���ƣ�Ĭ���б߿�����ʽΪ1
        self.wb = Workbook()
        self.ws = self.wb.add_sheet( sheet.decode('gbk') )
        self.col_num = 0 # ��ʼ�к�
        self.row_num = 0 # ��ʼ�к�
        self.ws.panes_frozen = True
        #self.ws.horz_split_pos = 1

        borders = Borders()
        borders.left = border_style
        borders.right = border_style
        borders.top = border_style
        borders.bottom = border_style
        
        
        pattern = Formatting.Pattern()
    ##--------------------------2009-2-7 14:42���ӱ���ı�����ɫ
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 0x17##�ٺ�
        
        self.style = XFStyle()
        self.style.borders = borders
        
        self.title_style = XFStyle()
        self.title_style.borders = borders
        self.title_style.pattern = pattern
        self.first_title_style = first_title_style()##������
        self.second_title_style = second_title_style()#�α���
        self.third_title_style = third_title_style()##�δα���
        self.content_style0 = content_style0()##������ʽ0
        self.content_style1 = content_style1()##������ʽ1
        
    
    
    
    
    
    def add_sheet( self, sheet ):
        # ����sheetҳ���û�ָ��sheet����
        self.ws = self.wb.add_sheet( sheet.decode('gbk') )
    
    def save( self, name ):
        # ����Excel���û�ָ���ļ���
        self.wb.save( name )
    
    #�����
    def first_title( self , item , col_begin , col_end ):
        """
        �ϲ�N��
        @param:item ---����
        @param:col_begin  �п�ʼ����
        @param:col_end  �н�������
        """
        self.ws.write_merge(self.row_num, self.row_num, col_begin, col_end, item.decode('gbk'), self.first_title_style)
        self.row_num += 1
    
    #������
    def second_title(self , item , col_begin , col_end):
        """
        �ϲ�N��
        @param:item ---����
        @param:col_begin  �п�ʼ����
        @param:col_end  �н�������
        """
        self.ws.write_merge(self.row_num, self.row_num, col_begin, col_end, item.decode('gbk'), self.second_title_style)
        self.row_num += 1
    #�δα���
    def third_title( self, fs, col = None, row = None ):
        # д��ͷ
        # ����û��Լ�ָ������row����col����ʹ���û�ָ������ϵ
        if not col: # ��(ÿд��һ�ж��ص���ʼ��)
            col = self.col_num
        if row: # ��(�б����ۼӣ��Ա㱨�����ݵ����)
            self.row_num = row
        
        for item in fs:
            self.ws.write(self.row_num, col, item.decode('gbk'), self.third_title_style)
            col += 1
        self.row_num += 1
        
    
    def title( self, fs, col = None, row = None ):
        # д��ͷ��Ŀǰֻ֧��һ�еı�ͷ
        # ����û��Լ�ָ������row����col����ʹ���û�ָ������ϵ
        if not col: # ��(ÿд��һ�ж��ص���ʼ��)
            col = self.col_num
        if row: # ��(�б����ۼӣ��Ա㱨�����ݵ����)
            self.row_num = row
        
        for item in fs:
            self.ws.write(self.row_num, col, item.decode('gbk'), self.title_style)
            col += 1
        self.row_num += 1
    
    #
    def content( self, lines, col = None, row = None ):
        # д���ݣ�lines����Ϊ������ʽ��[ [a, b, c,], [d, e, f], ]
        # ����û��Լ�ָ������row����col����ʹ���û�ָ������ϵ
        if not col: # ��(ÿд��һ�ж��ص���ʼ��)
            col = self.col_num
        if row: # ��(�б����ۼӣ��Ա㱨�����ݵ����)
            self.row_num = row
        
        for line in lines:
            thiscol = col
            for item in line:
                self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.style)
                thiscol += 1
            self.row_num += 1
    
    def content0( self, line, col = None, row = None ):
        # д���ݣ�lines����Ϊ������ʽ[a, b, c,]
        # ����û��Լ�ָ������row����col����ʹ���û�ָ������ϵ
        if not col: # ��(ÿд��һ�ж��ص���ʼ��)
            col = self.col_num
        if row: # ��(�б����ۼӣ��Ա㱨�����ݵ����)
            self.row_num = row
        
        thiscol = col
        for item in line:
            self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.content_style0)
            thiscol += 1
        self.row_num += 1
            
    def content1( self, line, col = None, row = None ):
        # д���ݣ�line����Ϊ������ʽ��[a, b, c,]
        # ����û��Լ�ָ������row����col����ʹ���û�ָ������ϵ
        if not col: # ��(ÿд��һ�ж��ص���ʼ��)
            col = self.col_num
        if row: # ��(�б����ۼӣ��Ա㱨�����ݵ����)
            self.row_num = row
        
        thiscol = col
        for item in line:
            self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.content_style1)
            thiscol += 1
        self.row_num += 1
    
#������ʽ
def title_style( ):
    style = content_style()
    style.font.bold = True
    #����ɫ-��ɫ
    pattern = Formatting.Pattern()
    ##--------------------------2009-2-7 14:42���ӱ���ı�����ɫ
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x17##�ٺ�
    style.pattern = pattern
    return style

def style_change_color():
    style1 = title_style()
    style1.font.bold = False
    style1.pattern.pattern_fore_colour = 0x3d##
    style2 = title_style()
    style2.font.bold = False
    style2.pattern.pattern_fore_colour = 0x3e##
    return style1 ,style2

##����
def frozen( ws , px=0 , py=0 ):
    
    ws.panes_frozen = True
    ws.horz_split_pos = px
    ws.vert_split_pos = py
    return ws
    
    
##������ʽҲ�ǻ�����ʽ
def content_style(  ):
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font
    style.borders = borders
    style.alignment = alignment
    return style


##��������ʽ
def first_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x0150##�ֺ�
    font.bold=True
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font  ##�ֺ�Ӧ�ô�һ��
    style.borders = borders##�ޱ���
    style.alignment = alignment#ˮƽ�ʹ�ֱ������
    return style
    
#��������ʽ
def second_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x00E0##�ֺ�
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x03#ˮƽ����
    alignment.vert = 0x01#��ֱ����
    
    style = XFStyle()
    style.font = font  ##�ֺ�Ӧ�ô�һ��
    style.borders = borders##�ޱ���
    style.alignment = alignment
    return style
    
#�δα�����ʽ
def third_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x00E0##�ֺ�
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x02#ˮƽ����
    alignment.vert = 0x01#��ֱ����
#    
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x2e##ǳ��ɫ-----to do
    
    style = XFStyle()
    style.font = font  ##�ֺ�Ӧ�ô�һ��
    style.borders = borders##�ޱ���
    style.alignment = alignment
    style.pattern = pattern
    return style


#ע��content_style0��content_style1��Ϊ��ɫ�������õ�
def content_style0():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01

    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font
    style.borders = borders
    style.alignment = alignment
    return style
    
def content_style1():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    ##��ɫֵ���Զ���pyExceleratoe�е�examples�µ�formate.xls
    #�߿�
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    pattern = Formatting.Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x1a## ˮ��ɫ------to do
    #����
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font
    style.borders = borders
    style.alignment = alignment
    style.pattern = pattern
    return style
    

    
#����excel
def outExcel( titlelist , contents   , filename ):##��Ҫ���ݵĲ����б�ͷ���� , ���� ���ļ���   excel
    myxls = XLS()
    myxls.title( titlelist )##д��ͷ
    myxls.content( contents )##д����
    path = os.path.join( settings.FILE_TEMP , filename)##���ļ�д���˷�������tempĿ¼�£�Ϊ�����ظ���ȡ�ļ���ʱ��Ӧȡ��ͬ�����֣�������uuid
    myxls.save( path )
    r = HttpResponse( file( path , 'rb' ).read() )
    r[ 'Content-Disposition' ] = 'attachment; filename="%s"' % filename
    r[ 'Content-Type' ] = 'application/octet-stream'
    return r
    
#����excel---��������⣺һ������⣬һ�������⣬һ����ͨ����
def outExcel3( title1 , title2 , titlelist , contents   , filename ):##��Ҫ���ݵĲ����б�ͷ���� , ���� ���ļ���   excel
    """
    @param:title1----������
    @param:title2----������
    @param:titlelist----�δα���
    @param:contents---����,��ɫ������ʾ
    @param:filename---�ļ���
    
    """
    myxls = XLS()
    myxls.first_title(  title1 , 0 , len(titlelist)-1 )
    myxls.second_title( title2 , 0 , len(titlelist)-1 )
    line = 2
    myxls.third_title( titlelist )##д��ͷ
    i = 0
    for items in contents:
        getattr(myxls, 'content%s'%(i%2))(items)
        i+=1

    path = os.path.join( settings.FILE_TEMP , filename)##
    myxls.save( path )
    r = HttpResponse( file( path , 'rb' ).read() )
    r[ 'Content-Disposition' ] = 'attachment; filename="%s"' % filename
    r[ 'Content-Type' ] = 'application/octet-stream'
    return r

#����excel---�ж�����⣺һ������⣬һ����ͨ����
def outExcel2( title1 , titlelist , contents   , filename ):##��Ҫ���ݵĲ����б�ͷ���� , ���� ���ļ���   excel
    """
    @param:title1----������
    @param:titlelist----�δα���
    @param:contents---����,��ɫ������ʾ
    @param:filename---�ļ���
    
    """
    myxls = XLS()
    myxls.first_title(  title1 , 0 , len(titlelist)-1 )
    myxls.third_title( titlelist )##д��ͷ
    i = 0
    for items in contents:
        getattr(myxls, 'content%s'%(i%2))(items)
        i+=1

    path = os.path.join( settings.FILE_TEMP , filename)##
    myxls.save( path )
    r = HttpResponse( file( path , 'rb' ).read() )
    r[ 'Content-Disposition' ] = 'attachment; filename="%s"' % filename
    r[ 'Content-Type' ] = 'application/octet-stream'
    return r


##
def test_2():
    wb = Workbook()
    ws0 = wb.add_sheet(u'test')
    a = first_title_style()#������
    b = second_title_style()#�α���
    c = third_title_style()##�δα���
    d = content_style0()##����0
    e = content_style1()##����1
    ws0.write_merge(0, 0, 0, 4, '���в����̻�����'.decode('gbk'), a)
    ws0.write_merge(1, 1, 0, 4, 'ͳ��ʱ��:2010��04��28��'.decode('gbk'), b )
    ws0.row(0).height = 0x0500
    ws0.row(1).height = 0x0100
    ws0.write(2, 0, '������'.decode('gbk'), c )
    ws0.write(2, 1, '�̻����'.decode('gbk'), c )
    ws0.write(2, 2, '�̻�����'.decode('gbk'), c )
    ws0.write(2, 3, '�ն���Դ'.decode('gbk'), c )
    ws0.write(2, 4, '�̻���ϵ��'.decode('gbk'), c )
    ws0.col(4).width = 0x0d00 
    ws0.col(3).width = 0x0c00 
    ws0.col(2).width = 0x0c00 
    ws0.col(1).width = 0x0c00 
    
    
    
    ws0.write(3, 0, 'aaa'.decode('gbk'), d )
    ws0.write(3, 1, 'bbb'.decode('gbk'), d )
    ws0.write(3, 2, 'ccc'.decode('gbk'), d )
    ws0.write(3, 3, 'ddd'.decode('gbk'), d )
    ws0.write(3, 4, 'eee'.decode('gbk'), d )
    
    ws0.write(4, 0, 'aaa'.decode('gbk'), e )
    ws0.write(4, 1, 'bbb'.decode('gbk'), e )
    ws0.write(4, 2, 'ccc'.decode('gbk'), e )
    ws0.write(4, 3, 'ddd'.decode('gbk'), e )
    ws0.write(4, 4, 'eee'.decode('gbk'), e )
    
    wb.save('222.xls')


if __name__ == '__main__':
    #test_1()
    #test_2()
    outExcel3( '���в����̻�����' , 'ͳ��ʱ��:2010��04��28��' , ['������','�̻����','�̻�����','�ն���Դ','�̻���ϵ��'] , [['a','b','c','d','e'],['a','b','c','d','e']]   , '333.xls' )