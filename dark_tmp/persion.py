# 测试类


class Persion(object):
    count = 0
    info = {
        'name': '小明'
    }
    info_list = []

    def __init__(self):
        self.name = '人'


if __name__ == '__main__':
    p = Persion()

    # p.count = 5
    # print(p.__dict__)
    # print(Persion.__dict__)
    # print(p.count)  # 5
    # print(Persion.count)  # 0


    p.count += 5
    print(p.__dict__)
    print(Persion.__dict__)
    print(p.count)  # 10
    print(Persion.count)  # 0


    # p.info['name'] = '小红'
    # print(p.__dict__)
    # print(Persion.__dict__)
    # print(p.info)  # {'name': '小红'}
    # print(Persion.info)  # {'name': '小红'}
    #
    p2 = Persion()

    # p2.info = {'name': 'Tom'}
    p2.info.update({'age':10})
    print(p2.__dict__)
    print(Persion.__dict__)
    print(p2.info)  # {'name': 'Tom'}
    print(Persion.info)  # {'name': '小红'}



    # print(p.info, Persion.info)
    # for i in range(10):
    #     p = Persion()
    #     p.info = {
    #         'name': 'test'
    #     }
    #     # p.info['name'] = '小红'
    #     print(p.info)
    #     print(Persion.info)
    #
    # x = Persion()
    # print('x--->', x.info)

    # print(p.info_list, Persion.info_list)
    # for i in range(10):
    #     p = Persion()
    #     # p.info_list = list('test')
    #     p.info_list.extend(list('test'))
    #     print('p-->', p.info_list)
    #     print('Persion-->', Persion.info_list)
    #
    # x = Persion()
    # print('x--->', x.info_list)
    #
    # i = 20
    # j = 20
    # print(id(i))
    # print(id(j))
    #
    # i += 1
    # print(id(i))
    #
    # d1 = [1, 2, 3]
    # d2 = [1, 2, 3]
    # print(id(d1))
    # print(id(d2))
    #
    # d1.append(4)
    # print(id(d1))


    p = Persion()

    p.count = 5
    print(p.count)  # 5
    print(id(p.count))  # 4375005952
    print(Persion.count)  # 0
    print(id(Persion.count))  # 4375005792  可以看到变量的引用变了

    p1 = Persion()

    p1.info['name'] = '小红'
    print(p1.info)  # {'name': '小红'}
    print(id(p1.info))  # 4376694288
    print(Persion.info)  # {'name': '小红'}
    print(id(Persion.info))  # 4376694288  变了的引用没有变

    p2 = Persion()

    p2.info = {'name': 'Tom'}
    print(p2.info)  # {'name': 'Tom'}
    print(id(p2.info))  # 4376693928  重新赋值，变量的引用不同
    print(Persion.info)  # {'name': '小红'}
    print(id(Persion.info))  # 4376694288  值变了，但引用没有变