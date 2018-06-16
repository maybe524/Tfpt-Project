#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os,json
# from list_ import do_ls

def do_rm(self, *args):
    cmd_split = args[0].split()
    filename = cmd_split[1]
    msg_dic={
            "directive": "rm",
            "filename": filename
            }
    #发送要创建的目录名和操作指令 
    self.client.send(json.dumps(msg_dic).encode())
    #收到服务端消息
    data = self.client.recv(1024).decode()
    print(data)
    if data == "remove_file_succeed":
        print("删除文件成功")
     
    elif data == "remove_file_defeated":
        print("文件删除失败，请检查")
    elif data == "file_no_exist":
        print("文件不存在")
