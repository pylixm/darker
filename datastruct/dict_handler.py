#coding=utf-8
"""
字典对象的有关操作
"""

class DictWrapper(dict):
    """一个字典，允许对象属性访问语法"""
    def __getattr__(self, name):
        try:
            value = self[name]
            if isinstance(value, dict) and not isinstance(value, DictWrapper):
                value = self[name] = DictWrapper(value)
            return value
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except KeyError:
            raise AttributeError(key)


def object2dict(obj):
    """object转换为字典对象"""
    return obj.__dict__
    
def getDictkeys( dic, keydic={}, n=1 ):
    """获取字典各层的key"""
    if isinstance(dic,dict):
        if not keydic.get(n):
            keydic.update( {n:dic.keys()} )
        else:
            keydic[n].extend( dic.keys() )
        n += 1 
        for value in dic.values():
            getDictkeys( value, keydic, n )
    return keydic 
    

class Object2dic(object):
    def __init__( self, name, age ):
        self.name = name
        self.age = age
        

if __name__=='__main__':
#    obj = Object2dic( 'pyli', 26)
#    print obj.name 
#    print type( obj )
#    dic = object2dict( obj )
#    print dic 
#    print type(dic)
    t_dic = {
                'leve1_1':{
                    'leve2_1':{
                        'leve3_1':{
                            'leve4_1':'1',
                            'leve4_2':'2'
                        }
                    },
                    'leve2_2':{
                        'leve3_2':{
                            'leve4_3':'1',
                            'leve4_4':'2'
                        }
                    }    
                }      
            }        
    print getDictkeys( t_dic )


