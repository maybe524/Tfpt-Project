#!/usr/bin/python3

import os,sys

L = []
def ls_folder(self, fileName):
    #的到ls  和文件夹名称
    #把字符串分割成字符串数组。以便好取值
    # msg_split = args[0].split()
    msg_split = fileName.split()
    action = msg_split[0]  #得到要操作的指令
    folder_name = msg_split[1]    #得到文件名

    msg_dir = "%s|%s"%(action,folder_name)

    #第一次通讯：发送标识符,文件名到服务器
    self.sockfd.send(msg_dir.encode())

    #服务器回复 Filelist_no_exit / Filelist_exit
    data = self.sockfd.recv(1024).decode()
    if data == 'Filelist_exit':
        data = self.sockfd.recv(4096).decode()
        files = data.split('|')
        files.remove('')

        for file in files:
            file_name = file.split(' ')

            FILE_NAME = file_name[0]
            FILE_EXT = file_name[1]
            FILE_DATE = file_name[2]+' '+file_name[3]
            FILE_SIZE = file_name[4]+' '+file_name[5]

            L.append([FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE])
        return L
        # print("文件列表展示完毕")
    # msg = input(">>>:")
    else:
        print("请求文件列表失败")
