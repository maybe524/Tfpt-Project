#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os,json

global folder

L = []
def do_ls(self):
    msg_dic={"directive": "list_"}
     #第一次通讯：发送标识符,文件名到服务器
    self.client.send(json.dumps(msg_dic).encode("utf-8"))

    #服务器回复 Filelist_no_exit / Filelist_exit
    data = self.client.recv(1024).decode()
    if data == 'Filelist_exit':
        data = json.loads(self.client.recv(4096).decode())

        for file in data:
            file_name = file.split(' ')

            FILE_NAME = file_name[0]
            FILE_EXT = file_name[1]
            FILE_DATE = file_name[2]+' '+file_name[3]
            FILE_SIZE = file_name[4]+' '+file_name[5]

            L.append([FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE])
            # print(FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE)
        return L
        # print("文件列表展示完毕")
    else:
        print("请求文件列表失败")