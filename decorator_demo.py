#!/usr/bin/python3
# @Time    : 2020/10/7
# @Author  : Yuhong Chen
# @Email   : yuhong3.chen@tcl.com

import time
import os
import sys
from functools import wraps


class Decorator():
    def __init__(self, func):
        print('类初始化')
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        print('进入装饰器')
        result = self.func(*args, **kwargs)
        self.count += 1
        return result


@Decorator
def request_page():
    '''
    request_page
    :return:
    '''
    print("访问一个网页")
    print("得到了response")


def count_all(*args, **kwargs):
    def count_time(func):
        """
        这是一个装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.process_time()
            num_list = func(*args, **kwargs)
            end_time = time.process_time()
            print("[{}]函数一共消耗了：{} 时间".format(
                str(func.__name__), str(end_time-start_time)))
            return num_list
        return wrapper
    print(*args, **kwargs)
    return count_time


@count_all("统计耗时：")
def get_even_num(num):
    num_list = []
    for i in range(1, num):
        if i % 2 == 0:
            num_list.append(i)
    return num_list


if __name__ == '__main__':
    # num = 1000000
    # num_list = get_even_num(num)
    request_page()
