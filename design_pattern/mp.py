# coding: utf8

"""
    并行计算模块
    原理：
        并行版本的实现说明:
        1 标准生产者\消费者模型
        2 生产者处于线程中, 将任务迭代器的内容写入任务队列中，并置结束标志
        3 消费者多个进程, 读取task_queue的内容, 并返回result到done_queue中
        4 主线程监控done_queue的内容, 并插入数据库(保持gInst的事务), 直到整个任务结束

"""

from multiprocessing import Process, Queue, current_process, cpu_count
import threading
import traceback
#from shangjie.utils import traceback2

def mp_start( n , iter , callback ):
    """
        多进程API
        参数：
            n           创建几个进程，当为0时，自动探测cpu个数，并创建N-1个
            iter        任务迭代器，可以直接迭代的对象。
                        list，tuple或含有yield的函数
                        每次迭代返回的内容应该为( func , args , kwargs )
                      * 注：
                            func函数必须为模块级函数，否则在子进程中无法正常调用
                            且func函数第一个参数为idx（子进程序号）
            callback    回调函数，每个任务函数返回值的处理。
                        开发人员应该根据任务函数定义。
                        当为空时，系统不处理回调。
                        回调函数的参数为：
                            子进程序号，函数返回结果
        返回值：
            无

        用法：
            在主线程中调用该函数，该函数调用前，需准备好任务迭代器和回调函数。
            该函数会阻塞，直到所有任务完成。
    """
    # 确定子进程个数
    if n == 0:
        n = cpu_count() - 1
        if n == 0:
            n = 1
    # 初始化工作队列和结果队列
    task_queue = Queue()
    done_queue = Queue()
    # 先启动消费者待命
    subs = []
    for i in range(n):
        p = Process( target=worker, args=( i , task_queue , done_queue ) )
        subs.append( p )
        p.daemon = False
        p.start()
    try:
        # 启动生产者线程
        import threading
        t = threading.Thread( target = publisher , args= ( n , iter , task_queue ) ).start()
        stops = 0
        ex = False
        while stops < n:
            result = done_queue.get()
            if result == 'STOP':
                stops += 1
            elif type( result ) is tuple and result[0] == 'EXCEPT':
                stops += 1
                ex = result[1]
            elif result and callable( callback ):
                callback( *result )
        if ex:
            raise RuntimeError( "并行处理时，子进程发生异常：\n%s" % ex )
    finally:
        # 清理所有子进程
        for p in subs:
            p.join()

def publisher( n , iter , task_queue ):
    """
        使用线程处理任务发生的原因是有可能iter是一个yield函数迭代器，内容可能会非常多。
    """
    try:
        for obj in iter:
            if type( obj ) is not tuple:
                raise RuntimeError( '任务迭代器应该返回元组对象[%r]' % obj )
            if len( obj ) != 3:
                raise RuntimeError( '任务迭代器应该返回三元素元组对象[%r]' % obj )
            if not callable( obj[0] ):
                raise RuntimeError( '任务的第一元素应该为可执行对象[%r]' % obj[0] )
            if type( obj[1] ) is not tuple:
                raise RuntimeError( '任务的第二元素应该为tuple[%r]' % obj[1] )
            if type( obj[2] ) is not dict:
                raise RuntimeError( '任务的第三元素应该为dict[%r]' % obj[2] )
            task_queue.put( obj )
    except:
        traceback.format_exc( )

    for i in range( n ):
        task_queue.put( 'STOP' ) # 发送给子进程结束信号

def worker( idx , task_queue , done_queue ):
    try:
        for func , args , kwargs in iter(task_queue.get, 'STOP'):
            result = func( idx , *args , **kwargs )
            done_queue.put( ( idx , result ) )
        done_queue.put( 'STOP' )
    except:
        ex = traceback.format_exc( )
        done_queue.put( ( 'EXCEPT' , ex ) )
    finally:
        import sys
        sys.exit(0)

# for test
# 由于sum函数需要在子进程中执行，因此，必须将其配置为模块级的
import time
def sum( idx , a , b ):
    r = 0
    if a == 5:
        raise RuntimeError( 'haha' )
    for i in range( 10 ):
        time.sleep( 0.1 )
        r += i
    return a

if __name__ == '__main__':
    # 测试
    def itt():
        for i in range( 10 ):
            yield ( sum , ( i , i * 10 ) , {} )

    def cb( idx , x ):
        print 'p' , idx , 'done' , x , time.time()

    import time
    t = time.time()
    print t
    mp_start( 5 , itt() , cb )
    print time.time() - t