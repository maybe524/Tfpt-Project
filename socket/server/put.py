#!/usr/bin/env python3
import os,json
from folder_size import *
from conf import PATH_

FILE_PATH = PATH_

def do_put(self, *args):
    cmd_dic = args[0]
    filename = cmd_dic["file_name"]  #文件名
    file_size = cmd_dic["file_size"] #文件大小
    file_type = cmd_dic["file_type"]
    # self.request.send(filename.encode())
    #定义用户家目录总大小
    HONE_MAX_SIZE = 10240000000
    #查看当前家目录磁盘空间大小
    dir_size = getdirsize(FILE_PATH)
    print("当前用户磁盘空间大小:%s" % dir_size)
    size_sum = dir_size + file_size
#--------------------------------------------
    if size_sum < HONE_MAX_SIZE:
        if file_type == "FILE": #开始接受文件
            #服务器判断用户家目录下面有没有这个文件和否是一个文件,来确认是否启用断点续传
            if not os.path.isfile(FILE_PATH + filename):
            #如果没有该文件，则发送准备好接收到服务端,开始接收(防止粘包)
                self.request.send("Start|0".encode())
                new_size = 0
                f = open(FILE_PATH + filename, 'wb')
                while new_size < file_size:
                    if file_size - new_size > 1024:
                        size = 1024
                    else:
                        size = file_size - new_size
                    data = self.request.recv(size)
                    new_size += len(data)
                    f.write(data)  #写入文件
                else:
                    f.close()
                    print("文件上传成功!")                    
            else:
                #如果本地存在此文件,将给服务端发送断点续传的请求标签
                #如果存在，则得到本地文件的大小，发送断点续传标识符，和本地文件大小到服务器，
                #以追加方式打开文件                
                native_size = os.path.getsize(FILE_PATH + filename)
                self.request.send(("Continue|%s"%native_size).encode())
                f = open(FILE_PATH + filename, 'ab')
                while native_size < file_size:
                    if file_size - native_size > 1024:
                        size = 1024
                    else:
                        size = file_size - native_size
                    data = self.request.recv(size)
                    native_size += len(data)
                    f.write(data)  #写入文件
                else:
                    f.close()
                    print("文件上传成功!")


        elif file_type == "FOLDER":
            self.request.send("start_folder".encode())
            data = json.loads(self.request.recv(4096).decode())
            for i in data:
                try:
                    os.makedirs(FILE_PATH + i)
                except FileExistsError:
                    pass
            else:
                try:
                    if os.path.exists(FILE_PATH + i):
                        print("文件夹创建完毕,开始接受文件")
                    else:
                        print("Error,")
                except:
                    pass  
                        
            self.request.send("start_file".encode())

            while True:
                file_ = self.request.recv(2048).decode()
                if file_ != "allfile_succee":
                    fi = file_.split(" ")
                    filename = fi[0]
                    file_size = int(fi[1])
                    f_size = 0
                    print("文件名:",filename, "大小",file_size)
                    sleep(0.2)
                    self.request.send("start_succeed".encode())
                    f = open(FILE_PATH + filename,'wb')
                    while f_size < file_size:
                        if file_size - f_size > 1024:
                            size = 1024
                        else:
                            size = file_size - f_size
                        data = self.request.recv(size)
                        f_size += len(data) 
                        f.write(data)  #写入文件
                    else:
                        f.close()
                    print("文件上传成功!")
                    sleep(0.2)
                    self.request.send("start_file_succeed".encode())
                    file_ok = self.request.recv(1024).decode()
                    if file_ok == "succee":
                        print("继续循环")
                        continue
                else:
                    print("文件夹接受完成")
                    break

    else:
        self.request.send("Home_size|0000".encode())
        print("家目录磁盘空间不足")