#!/usr/bin/python3
# -*- coding:utf-8 -*-

from s_conf import PATH_
import os,json

FILE_PATH = PATH_

def do_smkdir(self, *args):
    cmd_dic = args[0]
    filename = cmd_dic["file_name"]

    if not os.path.exists(FILE_PATH + filename):
        os.makedirs(FILE_PATH + filename)
        if os.path.exists(FILE_PATH + filename):
        	self.request.send("creation_folder_succeed".encode())
        else:
        	self.request.send("creation_folder_defeated".encode())
    else:
    	self.request.send("folder_exist".encode())


