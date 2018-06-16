#!/usr/bin/python3
from socket import *
from time import sleep
import os,sys
from get import client_get
from put import client_put
from List import *
from ls import *
# from progress import progress


#创建主client类
class FtpClient():

	def __init__(self,sockfd):
		self.sockfd = sockfd

	#文件列表展示
	def file_list(self):
		return client_list(self)

	def list_folder(self, fileName):
		return ls_folder(self, fileName)

	#文件下载
	def file_get(self, fileName, pgMemValue):
		return client_get(self, fileName, pgMemValue)

	#文件上传
	def file_put(self, fileName, pgbarChange):
		client_put(self, fileName, pgbarChange)


	# #进度条：
	# def file_progress(self):
	# 	progress(self, num, Sum, l)


	def do_quit(self):
		self.sockfd.send(b"Q")
		self.sockfd.close()
		sys.exit(0)

	def setFileRoot(self, path):
		self.path = path


# def main_run():

# 	HOST = "127.0.0.1"
# 	PORT = 8888
# 	ADDR = (HOST,PORT)
# 	BUFFERSIZE = 1024

# 	client_sockfd  = socket()
# 	client_sockfd.connect(ADDR)

   	#创建客户请求对象
   	
	# Client = FtpClient(client_sockfd)


# if __name__ == "__main__":
# 	run()









    # 客户端与服务端交户
	# while 1:
	# 	print("=======命令选项========")
	# 	print("1) 	 list 	 		  ")
	# 	print("2)  get file           ")
	# 	print("3)  put file           ")
	# 	print("4)	 quit             ")
	# 	print("=======================")
	# 	msg = input("输入命令:")

	# 	# if msg.strip() == 'list':
	# 	# 	Client.file_list()

	# 	if msg[:3] == "get":
	# 	# elif startswith("get"):
	# 		# Filename = data.split(' ')[-1]
	# 		Client.file_get(msg)

	# 	elif msg[:3] == "GET":
	# 	# elif startswith("get"):
	# 		# Filename = data.split(' ')[-1]
	# 		Client.get_continue(msg)

	# 	elif msg[:3] == "put":
	# 		# Filename = data.split(' ')[-1]
	# 		Client.file_put(msg)

	# 	elif msg.strip() == "quit":
	# 		Client.do_quit()

	# 	else:
	# 		print("请输入正确的命令!!!")

