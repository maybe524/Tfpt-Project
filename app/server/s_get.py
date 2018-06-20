#!/usr/bin/env python3
from time import sleep
from s_conf import PATH_
import os,json
import re


FILE_PATH = PATH_

def do_sget(self, *args):
    cmd_dic = args[0]
    file_name = cmd_dic["file_name"]
    print(file_name)
    # self.request.send(filename.encode())
    #-----------------------------------------------------------------------
    file_n = FILE_PATH + file_name
    print(file_n)
    if os.path.exists(file_n):
          #判断是否是文件夹
        if not os.path.isdir(file_n):
            #如果是一个文件,发送文件表示到客户端
            self.request.send("PUT_FILE".encode())
            #得到文件总大小
            file_size = os.stat(file_n).st_size
            msg_dic = "%s|%s"%(file_size,file_name)
            # 发送文件总大小，和文件目录
            sleep(0.5)
            self.request.send(msg_dic.encode())
            #确定客户端信息，判断是直接发送还是断点续传
            client_response = self.request.recv(1024).decode()
            #得到客户端发来标识符，
            client_get = client_response.split('|')[0] 
            #得到客户端文件大小
            new_size = int(client_response.split('|')[1])       
    #-----------------------------------------------------------------------
            f = open(file_n, 'rb')
            #判断是否执行断点续传
            if client_get == "start": #发送总文件
                #开始循环发送文件
                for line in f:
                    self.request.send(line)
                    # new_size += len(line)
                else:
                    print("文件上传至客户成功！")
                f.close() #关闭文件
    #-----------------------------------------------------------------------
            elif client_get == "Continue": #断点续传
                #使用seek方法来实现将文件指针放在上次断点处，并继续传输，进而完成断点续传的功能，第一个参数表示指针偏移位数，第二个参数表示，从文件开头开偏移
                #使用seek方法来实现将文件指针重置
                f.seek(new_size,0)
                #开始循环发送文件
                for line in f:
                    self.request.send(line)
                    # new_size += len(line)
                else:
                    print("文件上传至客户成功！")
                f.close() #关闭文件
    #-----------------------------------------------------------------------
        else:
            #发送put_folde到服务器,开始传输文件夹
            self.request.send("PUT_FOLDER".encode())
            File = []
            File_pa = []
            def folder(file_n):
            #遍历file_name下所有文件，包括子目录  
                files = os.listdir(file_n)
                for fi in files:
                    fi_d = os.path.join(file_n,fi)
                    if os.path.isdir(fi_d):
                        folder(fi_d)
                        fi_ = "".join(re.findall("%s\S+" % file_name, fi_d))
                        File_pa.append(fi_)  #得到所有目录  
                    else:
                        f_name = os.path.join(file_n,fi_d) #得到所有文件
                        fi_f = "".join(re.findall("%s\S+" % file_name, f_name))
                        File.append(fi_f)

            folder(file_n)
            
            for i in range(len(File)-1,-1,-1):
                if File[i] == '':
                    File.remove('')
            for i in range(len(File_pa)-1,-1,-1):
                if File_pa[i] == '':
                    File_pa.remove('')

            client_folder = self.request.recv(1024).decode()
            #发送所有文件夹
            if client_folder == "start_folder":
                self.request.send(json.dumps(File_pa).encode())
            #发送所有文件
            client_file = self.request.recv(1024).decode()
            if client_file == "start_file":
                print("发送文件")
                #开始循环发送文件
                for f in File:
                    sleep(0.3)
                    file_size = os.stat(FILE_PATH + f).st_size  #得到文件大小
                    f_s = "%s %s"%(f,file_size)
                    print("+=====",f_s)
                    self.request.send(f_s.encode())
                    client_ = self.request.recv(1024).decode()
                    fi = f.split(" ")[0]
                    f = open(FILE_PATH + fi, 'rb')
                    #开始循环发送文件
                    for line in f:
                        self.request.send(line)
                    else:
                        f.close()
                        sleep(0.2)
                    file_ok = self.request.recv(1024).decode()
                    print(file_ok)
                    self.request.send("succee".encode())
                    sleep(0.2)

                else:
                    self.request.send("allfile_succee".encode())
    else:
        self.request.send("400".encode())

 