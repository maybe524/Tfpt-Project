#!/usr/bin/python3
import os,sys
import json
import hashlib
from progress import progres


FILE_PATH = "/data/new_ftp/client_data/"
# print(FILE_PATH)

def __client_put(self, fileName, pgbarChange):

	#客户端上传功能
	cmd_split = fileName.split()
	action = cmd_split[0]  #要操作的指令
	file_name = cmd_split[1]  #需要上传的文件


	#判断用户本地上传目录下面有没有这个文件和否是一个文件
	if os.path.isfile(FILE_PATH + file_name):
		#如果有这个文件：得到文件总大小
		file_size = os.stat(FILE_PATH + file_name).st_size
		print(file_size)
		#发送操作指令文件名，文件大小到服务器
		msg_dic = "%s %s %s"%(action,file_name,file_size)
		#第一次通讯，发送操作指令，文件，文件大小
		self.sockfd.send(msg_dic.encode())
		# 防止粘包，等服务器确认
		server_response = self.sockfd.recv(1024).decode()
		client_tag = server_response.split('|')[0]
		server_file_size = int(server_response.split('|')[1])

		#打开文件
		with open(FILE_PATH + file_name,'rb') as f:
			##判断是否准备好,如果是start，这开始从头发送文件，
			M = hashlib.md5()       #生成md5对象
			if client_tag == "start": 
				new_size = 0  #设置文件初始大小为0 
				#开始循环发送文件
				for line in f:
					self.sockfd.send(line)
					send_size = f.tell()   #获取当前指针位置（字节）,以来显示进度条
					# progres(self, send_size, file_size,50)

					def progerss(new_size, file_size):
						percent = float(new_size) / float(file_size)
						new_percent = percent * 100
						return new_percent

					def progerss1():
						return progerss(new_size, file_size)
					if temp != int(progerss1()):
						temp = int(progerss1())
						pgbarChange(temp)


					M.update(line)
					# new_size += len(line)
				else:
					print()
					print("file upload success")
					f.close()
					client_file_md5 = M.hexdigest()
					server_file_md5 = self.sockfd.recv(1024).decode()
					print("服务器 file md5:", server_file_md5)
					print("客户端 file md5:", client_file_md5)

			elif client_tag == "Continue":
				new_size = server_file_size
				f.seek(new_size,0)
				for line in f:  #循环继续发送
					self.sockfd.send(line)

					new_size += len(line)

					def progerss(new_size, file_size):
						percent = float(new_size) / float(file_size)
						new_percent = percent * 100
						return new_percent

					def progerss1():
						return progerss(new_size, file_size)
					if temp != int(progerss1()):
						temp = int(progerss1())
						pgbarChange(temp)

					# progres(self, new_size, file_size,50)
					M.update(line)
				else:
					# progres(self, new_size, file_size,50)

					def progerss(new_size, file_size):
						percent = float(new_size) / float(file_size)
						new_percent = percent * 100
						return new_percent

					def progerss1():
						return progerss(new_size, file_size)
					if temp != int(progerss1()):
						temp = int(progerss1())
						pgbarChange(temp)	
										
					print()
					print("文件继续上传至服务器成功！")
					f.close()
					client_file_md5 = M.hexdigest()
					server_file_md5 = self.sockfd.recv(1024).decode()
					print("服务器 file md5:", server_file_md5)
					print("客户端 file md5:", client_file_md5)												

			elif client_tag == '402':
				print("家目录磁盘空间不足!")			
	else:
		print("文件不存在！")				

def client_put(self, fileName, pgbarChange):
	p1 = Process(name = 'block',target = __client_put, args=(self, fileName, pgbarChange))
	p1.start()