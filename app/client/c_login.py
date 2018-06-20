#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import json
import re
from progress import *
from c_conf import PATH_

def do_clogin(self, *args):
    ret = False
    if len(args) < 2:
        print('args len is less than 2!')
        return False
    userName = args[0]
    passWord = args[1]
    if not userName or not passWord:
        print('user name or password is null!')
        return False

    msgDict = {
        'directive': 'login',
        'user_name': userName,
        'pass_word': passWord
    }
    print('do_clogin')
    self.client.send(json.dumps(msgDict).encode())
    msgRect = self.client.recv(1024).decode()
    if not msgRect:
        ret = False
    else:
        retDict = json.loads(msgRect)
        if retDict['login_result'] == 'OK':
            ret = True
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
          msgRect, ret)

    return ret