#!/usr/bin/python3
# -*- coding:utf-8 -*-
from time import sleep
from s_conf import PATH_
import os,json
import time
import sys
import re

def do_slogin(self, sqlFd, *args):
    logResult = 'FAIL'
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), args)
    if sqlFd and args:
        try:
            userName = args[0]['user_name']
            passWord = args[0]['pass_word']
            ret = sqlFd.mysqlLogin(userName, passWord)
            print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
                  'userName: ', userName, \
                  'passWord: ', passWord, \
                  'ret: ', ret)
            if not ret:
                logResult = 'OK'
        except Exception as e:
            print(e)
    retDict = {
        'login_result': logResult
    }
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
          logResult)
    self.request.send(json.dumps(retDict).encode())