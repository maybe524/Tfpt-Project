#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os, sys
import signal
from time import sleep
import socketserver
import json

from s_conf import *
from s_sqlgen import *
from s_list import do_sls
from s_rm import do_srm
from s_cd import do_scd
from s_get import do_sget
from s_put import do_sput
from s_mkdir import do_smkdir
from s_rename import do_srename
from s_login import do_slogin
from s_register import do_sregister

timeout = 60     # 设置超时时间变量 

client_addr = []
client_socket = []
tftpSql = None

class MyTCPHandler(socketserver.BaseRequestHandler):
    allow_reuse_address = True
    daemon_threads = True
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    def setup(self):  
        self.ip = self.client_address[0].strip()     # 获取客户端的ip  
        self.port = self.client_address[1]           # 获取客户端的port  
        self.request.settimeout(timeout)        # 对socket设置超时时间 
        print(self.ip+":"+str(self.port)+"连接到服务器！")
        client_addr.append(self.client_address) # 保存到队列中  
        client_socket.append(self.request)      # 保存套接字socket 

    def handle(self):  #所有请求的交互都是在handle里执行的,
        while True:
            try:
                data = self.request.recv(1024).strip()#每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler)
                if not data:
                    print('Client disconnet, so break handle!')
                    break
                #获取客户端操作指令和文件名
                cmd_dic = json.loads(data.decode())
                print("data = ",cmd_dic)
                directive = cmd_dic["directive"]
                print("directive = ", directive)

                if hasattr(self, directive):
                    func = getattr(self, directive)
                    func(cmd_dic)
                else:
                    print("Error")
                
            except ConnectionResetError as e:
                print("Error----2")
                break
            # except:
            #     print(self.ip+":"+str(self.port)+"接收超时！即将断开连接！")
            #     # self.request.send("连接超时，已断开连接.".encode())
            #     break

    def finish(self): 
        sleep(2)
        print(self.ip+":"+str(self.port)+"断开连接！")  
        client_addr.remove(self.client_address)  
        client_socket.remove(self.request)

    def list(self, *args):
        do_sls(self, *args)

    def cd(self, *args):
        do_scd(self, *args)

    def get(self, *args):
        do_sget(self, *args)

    def put(self, *args):
        do_sput(self, *args)

    def mkdir(self, *args):
        do_smkdir(self, *args)

    def rename(self, *args):
        do_srename(self, *args)

    def rm(self, *args):
        do_srm(self, *args)

    def login(self, *args):
        do_slogin(self, tftpSql, *args)

    def register(self, *args):
        do_sregister(self, tftpSql, *args)

'''
Add for do prepare work befor server is start up!
Huangxiaowen
2018.6.16
'''
def serverPrepare():
    if not os.path.exists(PATH_):
        os.mkdir(PATH_)

    global tftpSql
    tftpSql = TftpMysql("localhost", 3306, "user", "root", "xiao404040")
    tftpSql.open()
    print('server prepare done!')

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8889

    serverPrepare()

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
    server.serve_forever()
    tftpSql.close()

