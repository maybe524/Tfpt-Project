#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os,json
from s_conf import PATH_

FILE_PATH = PATH_

def do_srename(self, *args):
    cmd_dic = args[0]
    filename = cmd_dic["file_name"]
    new_filename = cmd_dic["new_filename"]

    if not os.path.exists(FILE_PATH + new_filename):
        os.rename(FILE_PATH + filename, FILE_PATH + new_filename)
        if os.path.exists(FILE_PATH + new_filename):
            self.request.send("file_rename_succeed".encode())
        else:
            self.request.send("file_rename_defeated".encode())
    else:
        self.request.send("file_name_exist".encode())
