#!/usr/bin/python3
# -*- coding:utf-8 -*-
from time import sleep
from s_conf import PATH_
import os,json
import time
import sys
import re

def do_sregister(self, sqlFd, *args):
    regResult = 'FAIL'
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), args)
    if sqlFd and args:
        try:
            userName = args[0]['user_name']
            passWord = args[0]['pass_word']
            ret = sqlFd.mysqlRigester(userName, passWord)
            print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
                  'userName: ', userName, \
                  'passWord: ', passWord, \
                  'ret: ', ret)
            if not ret:
                regResult = 'OK'
        except Exception as e:
            print(e)
    retDict = {
        'register_result': regResult
    }
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
          regResult)
    self.request.send(json.dumps(retDict).encode())