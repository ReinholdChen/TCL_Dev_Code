#!/usr/bin/python3
# @Time    : 2020/10/7
# @Author  : Yuhong Chen
# @Email   : yuhong3.chen@tcl.com

import time
import os
import sys
from functools import wraps


class Decorator(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance, value):
        self.fset(instance, value)

    def __delete__(self, instance):
        self.fdel(instance)

    def getter(self, fget):
        return Decorator(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return Decorator(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return Decorator(self.fget, self.fset, fdel, self.__doc__)


class Target(object):

    desc = "Amazing pyhton"

    def __init__(self, attr=5):
        self._x = attr

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = Decorator(getx, setx, delx, desc)
