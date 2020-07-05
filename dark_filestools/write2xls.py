# coding: gbk
"""
本程序简单封装pyExcelerator模块，实现了XLS类，用户可通知这个类创建Excel报表
基本使用方式：
    1.创建实例：myxls = XLS()
    2.写表头：myxls.title( ['行员代码', '行员姓名', '机构代码', '机构名称'] )
    3.写表体：myxls.content( [ ['0001', '张三', '01', '办公室'], ['0002', '李四', '02', '科技部'], ] )
    4.保存：myxls.save( 'my.xls' )
不足：
    1.样式单一：目前只是全部默认为有边框，没有设置其他任何样式
    2.无公式项：没有创建“累加”、“平均”等公式项的接口
    3.格式单一：内容全部为字符串，无法通过拖拽累计求和
    4.表头、表体没有统一限定：目前允许表头列数与表体不对应
"""
from pyExcelerator import *
import os 
from django.http import HttpResponseRedirect, HttpResponse
from shangjie.conf import settings

class XLS:
    def __init__( self, sheet = 'Sheet1', border_style = 1 ):
        # 创建Excel对象，用户指定sheet名称，默认有边框且样式为1
        self.wb = Workbook()
        self.ws = self.wb.add_sheet( sheet.decode('gbk') )
        self.col_num = 0 # 起始列号
        self.row_num = 0 # 起始行号
        self.ws.panes_frozen = True
        #self.ws.horz_split_pos = 1

        borders = Borders()
        borders.left = border_style
        borders.right = border_style
        borders.top = border_style
        borders.bottom = border_style
        
        
        pattern = Formatting.Pattern()
    ##--------------------------2009-2-7 14:42增加标题的背景颜色
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 0x17##嘿嘿
        
        self.style = XFStyle()
        self.style.borders = borders
        
        self.title_style = XFStyle()
        self.title_style.borders = borders
        self.title_style.pattern = pattern
        self.first_title_style = first_title_style()##主标题
        self.second_title_style = second_title_style()#次标题
        self.third_title_style = third_title_style()##次次标题
        self.content_style0 = content_style0()##内容样式0
        self.content_style1 = content_style1()##内容样式1
        
    
    
    
    
    
    def add_sheet( self, sheet ):
        # 增加sheet页，用户指定sheet名称
        self.ws = self.wb.add_sheet( sheet.decode('gbk') )
    
    def save( self, name ):
        # 保存Excel，用户指定文件名
        self.wb.save( name )
    
    #大标题
    def first_title( self , item , col_begin , col_end ):
        """
        合并N列
        @param:item ---内容
        @param:col_begin  列开始坐标
        @param:col_end  列结束坐标
        """
        self.ws.write_merge(self.row_num, self.row_num, col_begin, col_end, item.decode('gbk'), self.first_title_style)
        self.row_num += 1
    
    #副标题
    def second_title(self , item , col_begin , col_end):
        """
        合并N列
        @param:item ---内容
        @param:col_begin  列开始坐标
        @param:col_end  列结束坐标
        """
        self.ws.write_merge(self.row_num, self.row_num, col_begin, col_end, item.decode('gbk'), self.second_title_style)
        self.row_num += 1
    #次次标题
    def third_title( self, fs, col = None, row = None ):
        # 写表头
        # 如果用户自己指定了行row与列col，则使用用户指定的体系
        if not col: # 列(每写完一行都回到起始列)
            col = self.col_num
        if row: # 行(行必须累加，以便报表内容的输出)
            self.row_num = row
        
        for item in fs:
            self.ws.write(self.row_num, col, item.decode('gbk'), self.third_title_style)
            col += 1
        self.row_num += 1
        
    
    def title( self, fs, col = None, row = None ):
        # 写表头，目前只支持一行的表头
        # 如果用户自己指定了行row与列col，则使用用户指定的体系
        if not col: # 列(每写完一行都回到起始列)
            col = self.col_num
        if row: # 行(行必须累加，以便报表内容的输出)
            self.row_num = row
        
        for item in fs:
            self.ws.write(self.row_num, col, item.decode('gbk'), self.title_style)
            col += 1
        self.row_num += 1
    
    #
    def content( self, lines, col = None, row = None ):
        # 写内容，lines必须为如下形式：[ [a, b, c,], [d, e, f], ]
        # 如果用户自己指定了行row与列col，则使用用户指定的体系
        if not col: # 列(每写完一行都回到起始列)
            col = self.col_num
        if row: # 行(行必须累加，以便报表内容的输出)
            self.row_num = row
        
        for line in lines:
            thiscol = col
            for item in line:
                self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.style)
                thiscol += 1
            self.row_num += 1
    
    def content0( self, line, col = None, row = None ):
        # 写内容，lines必须为如下形式[a, b, c,]
        # 如果用户自己指定了行row与列col，则使用用户指定的体系
        if not col: # 列(每写完一行都回到起始列)
            col = self.col_num
        if row: # 行(行必须累加，以便报表内容的输出)
            self.row_num = row
        
        thiscol = col
        for item in line:
            self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.content_style0)
            thiscol += 1
        self.row_num += 1
            
    def content1( self, line, col = None, row = None ):
        # 写内容，line必须为如下形式：[a, b, c,]
        # 如果用户自己指定了行row与列col，则使用用户指定的体系
        if not col: # 列(每写完一行都回到起始列)
            col = self.col_num
        if row: # 行(行必须累加，以便报表内容的输出)
            self.row_num = row
        
        thiscol = col
        for item in line:
            self.ws.write(self.row_num, thiscol, item.decode('gbk'), self.content_style1)
            thiscol += 1
        self.row_num += 1
    
#标题样式
def title_style( ):
    style = content_style()
    style.font.bold = True
    #背景色-棕色
    pattern = Formatting.Pattern()
    ##--------------------------2009-2-7 14:42增加标题的背景颜色
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x17##嘿嘿
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

##冻结
def frozen( ws , px=0 , py=0 ):
    
    ws.panes_frozen = True
    ws.horz_split_pos = px
    ws.vert_split_pos = py
    return ws
    
    
##内容样式也是基础样式
def content_style(  ):
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    #对齐
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font
    style.borders = borders
    style.alignment = alignment
    return style


##主标题样式
def first_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x0150##字号
    font.bold=True
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    #对齐
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font  ##字号应该大一点
    style.borders = borders##无边线
    style.alignment = alignment#水平和垂直均居中
    return style
    
#副标题样式
def second_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x00E0##字号
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    #对齐
    alignment = Formatting.Alignment()
    alignment.horz = 0x03#水平均右
    alignment.vert = 0x01#垂直居中
    
    style = XFStyle()
    style.font = font  ##字号应该大一点
    style.borders = borders##无边线
    style.alignment = alignment
    return style
    
#次次标题样式
def third_title_style():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    font.height = 0x00E0##字号
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    #对齐
    alignment = Formatting.Alignment()
    alignment.horz = 0x02#水平均右
    alignment.vert = 0x01#垂直居中
#    
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x2e##浅紫色-----to do
    
    style = XFStyle()
    style.font = font  ##字号应该大一点
    style.borders = borders##无边线
    style.alignment = alignment
    style.pattern = pattern
    return style


#注：content_style0和content_style1是为颜色相间耳设置的
def content_style0():
    font = Font()
    font.name='Arial'
    font.colour_index =0x08
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01

    #对齐
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
    ##颜色值可以对照pyExceleratoe中的examples下的formate.xls
    #边框
    borders = Borders()
    borders.left = 0x01
    borders.right = 0x01
    borders.top = 0x01
    borders.bottom = 0x01
    pattern = Formatting.Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x1a## 水粉色------to do
    #对齐
    alignment = Formatting.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01
    
    style = XFStyle()
    style.font = font
    style.borders = borders
    style.alignment = alignment
    style.pattern = pattern
    return style
    

    
#导出excel
def outExcel( titlelist , contents   , filename ):##需要传递的参数有表头内容 , 内容 ，文件名   excel
    myxls = XLS()
    myxls.title( titlelist )##写表头
    myxls.content( contents )##写内容
    path = os.path.join( settings.FILE_TEMP , filename)##将文件写到了服务器的temp目录下，为避免重复，取文件名时，应取不同的名字，可以用uuid
    myxls.save( path )
    r = HttpResponse( file( path , 'rb' ).read() )
    r[ 'Content-Disposition' ] = 'attachment; filename="%s"' % filename
    r[ 'Content-Type' ] = 'application/octet-stream'
    return r
    
#导出excel---有三组标题：一个大标题，一个副标题，一个普通标题
def outExcel3( title1 , title2 , titlelist , contents   , filename ):##需要传递的参数有表头内容 , 内容 ，文件名   excel
    """
    @param:title1----主标题
    @param:title2----副标题
    @param:titlelist----次次标题
    @param:contents---内容,颜色交叉显示
    @param:filename---文件名
    
    """
    myxls = XLS()
    myxls.first_title(  title1 , 0 , len(titlelist)-1 )
    myxls.second_title( title2 , 0 , len(titlelist)-1 )
    line = 2
    myxls.third_title( titlelist )##写表头
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

#导出excel---有二组标题：一个大标题，一个普通标题
def outExcel2( title1 , titlelist , contents   , filename ):##需要传递的参数有表头内容 , 内容 ，文件名   excel
    """
    @param:title1----主标题
    @param:titlelist----次次标题
    @param:contents---内容,颜色交叉显示
    @param:filename---文件名
    
    """
    myxls = XLS()
    myxls.first_title(  title1 , 0 , len(titlelist)-1 )
    myxls.third_title( titlelist )##写表头
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
    a = first_title_style()#主标题
    b = second_title_style()#次标题
    c = third_title_style()##次次标题
    d = content_style0()##内容0
    e = content_style1()##内容1
    ws0.write_merge(0, 0, 0, 4, '本行不良商户名单'.decode('gbk'), a)
    ws0.write_merge(1, 1, 0, 4, '统计时间:2010年04月28日'.decode('gbk'), b )
    ws0.row(0).height = 0x0500
    ws0.row(1).height = 0x0100
    ws0.write(2, 0, '档案号'.decode('gbk'), c )
    ws0.write(2, 1, '商户编号'.decode('gbk'), c )
    ws0.write(2, 2, '商户名称'.decode('gbk'), c )
    ws0.write(2, 3, '终端来源'.decode('gbk'), c )
    ws0.write(2, 4, '商户联系人'.decode('gbk'), c )
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
    outExcel3( '本行不良商户名单' , '统计时间:2010年04月28日' , ['档案号','商户编号','商户名称','终端来源','商户联系人'] , [['a','b','c','d','e'],['a','b','c','d','e']]   , '333.xls' )