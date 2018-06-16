#!/usr/bin/python3
# -*- coding:utf-8 -*-

import signal
from time import sleep
import socketserver
import json
from list_ import do_ls
from rm import do_rm
from cd import do_cd
from get import do_get
from put import do_put
from mkdir import do_mkdir
from rename import do_rename

timeout = 60     # 设置超时时间变量 

client_addr = []
client_socket = []


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
                self.data = self.request.recv(1024).strip()#每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler)
                #获取客户端操作指令和文件名
                cmd_dic = json.loads(self.data.decode())
                # print("data=",cmd_dic)
                directive = cmd_dic["directive"]

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

    def list_(self, *args):
        do_ls(self, *args)

    def cd(self, *args):
        do_cd(self, *args)

    def get(self, *args):
        do_get(self, *args)

    def put(self, *args):
        do_put(self, *args)

    def mkdir(self, *args):
        do_mkdir(self, *args)

    def rename(self, *args):
        do_rename(self, *args)

    def rm(self, *args):
        do_rm(self, *args)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8889
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
    server.serve_forever()

