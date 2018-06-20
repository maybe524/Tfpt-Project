#!/usr/bin/env python3

from s_list import *
from time import sleep
from s_conf import PATH_
import os,json
import re

FILE_PATH = PATH_
print("jiamulu >>>",FILE_PATH)

def do_scd(self, *args):
    cmd_dic = args[0]
    filename = cmd_dic["file_name"]
    print("filename",filename)
    # self.request.send(filename.encode())
    f_pash = []
    f_list = os.listdir(FILE_PATH + filename)
    if not f_list:
        self.request.send("Filelist_no_exit".encode())
        return
    else:
        self.request.send("Filelist_exit".encode())
    sleep(0.02)  #防止粘包

    for i in f_list:
        if i.startswith('.'):
            continue
        pa = filename + i
        file_all = "%s %s %s %s"%(pa, file_form(pa), file_date(pa), file_max(pa))
        f_pash.append(file_all)

	#发送家目录所有目录
    self.request.send(json.dumps(f_pash).encode())
  
