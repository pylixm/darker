from multiprocessing import Process
import os
import time


# 子进程要执行的代码
def run_proc(name):
    for i in range(3):
        print('Run child process %s (%s)...' % (name, os.getpid()))
        time.sleep(1)


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Process will start.')
    p.start()
    # p.join()  # 等待子进程完成后，再退出主进程
    print('Process end.')
