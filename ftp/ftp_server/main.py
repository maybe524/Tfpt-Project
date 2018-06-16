#!/usr/bin/python3
from socket import *
from time import sleep
import os,sys
import signal
import json
from deal_list import server_deal_get
from deal_get import server_deal_list
from deal_put import server_deal_put
from deal_folder import server_deal_folder


class TftpServer():

    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        deal_list.server_deal_list(self)


    def do_folder(self,*args):
        deal_folder.server_deal_folder(self, *args)

    #处理客户端下载文件的请求
    def do_get(self, *args):
        deal_get.server_deal_get(self, *args)

    #处理客户端上传文件的请求
    def do_put(self, *args):
        deal_put.server_deal_put(self, *args)


def run(ADDR):
    BUFFERSIZE = 1024
    #创建套接字
    server_sockfd  = socket()
    #设置端口立即重用
    server_sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定 IP 和端口号
    server_sockfd.bind(ADDR)
    #监听套接字
    server_sockfd.listen(5)
    #处理僵死进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            #阻塞等待客户端连接
            connfd, addr = server_sockfd.accept()
        except KeyboardInterrupt:
            server_sockfd.close()
            sys.exit(0)
        except Exception:
            continue
    	#此处写入日志
        print("有新客户端登录:",addr)
    	#使用父子进程，父进程处理后端，子进程负责接受客户端
        pid = os.fork()
        if pid < 0:
            print("创建子进程失败")
            connfd.close()
            continue  #继续等待连接

        elif pid == 0:
            server_sockfd.close()
            #创建客户端通信对象
            Server = TftpServer(connfd)
            while True:
            	#接受客户端的请求类型,判断调用什么模块
                data = connfd.recv(BUFFERSIZE).decode()
                # print("data===",data)
                
                if data == 'LIST':
                    Server.do_list()
                elif data[:2] == "ls" or data[:2] == "ll":
                    Server.do_folder(data)                

                elif data[:3] == 'get':
                    Server.do_get(data)

                elif data.split('|')[0] == 'GET':
                    Server.get_server_continue(data)

                elif data[:3] == 'put':
                    Server.do_put(data)

                elif data[:4] == 'QUIT':
                    print("客户端退出",addr)
                    sys.exit(0)                     

        else:
            connfd.close()
            continue


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8888
    ADDR = (HOST,PORT)
#调用主程
    run(ADDR)





