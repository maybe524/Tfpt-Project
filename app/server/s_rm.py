#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os,sys
import json
from s_conf import PATH_

FILE_PATH = PATH_

def do_srm(self, *args):
    cmd_dic = args[0]
    filename = cmd_dic["filename"]

    print(FILE_PATH + filename)

    if os.path.exists(FILE_PATH + filename):
        os.popen("rm -rf %s"%(FILE_PATH + filename))
        if os.path.exists(FILE_PATH + filename):
            self.request.send("remove_file_succeed".encode())
        else:
            self.request.send("remove_file_defeated".encode())
    else:
        self.request.send("file_no_exist".encode())

