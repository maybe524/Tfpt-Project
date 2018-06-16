#!/usr/bin/python3
import os,sys
import socket
import hashlib
import json
# from core import progress
from time import *
from multiprocessing import Event,Process

FILE_PATH = "/data/new_ftp/client_data/"

#客户端下载功能
def __client_get(self, fileName, pgMemValue):
	'''
	收到用户给定的指定码和文件：*args (星号元组传参)方便后续加功能
	格式： get file_name
	msg_all = args
	action = args[0]  #动作
	file_name = args[1]
	'''
	#把字符串分割成字符串数组。以便好取值
	msg_split = fileName.split()
	action = msg_split[0]  #得到要操作的指令
	file_name = msg_split[1]	#得到文件名
	# file_name_size = msg_split[2] #得到文件大小，如果有的话
	# file_name_path = msg_split[3] #得到文件路径

	msg_dir = "%s|%s"%(action,file_name)

	#第一次通讯：发送标识符,文件名到服务器
	self.sockfd.send(msg_dir.encode())

	#第二次通讯：客户端收到服务端发送的信息（文件大小，和存不存在标识码）
	msg_d = self.sockfd.recv(1024).decode()
	print("===",msg_d)
	#判断收到服务器开始发送文件开始文件夹
	if msg_d == "PUT_FILE":  #收到的是文件,开始发送文件
		self.sockfd.send("准备接收文件".encode())
		msg = self.sockfd.recv(1024).decode()
		# 得到标识码和文件大小
		server_response = msg.split('|')
		file_total_size = int(server_response[0])  #文件总大小
		file_exist = server_response[1]  #存在标识码，存在则为 200
	
		# print(server_response)
		#判断服务器发过来的标识符是否和客户端相同，
		if file_exist == "200":
			#通过判断本地是否有此文件，来确认是否启用断点续传
			if not os.path.isfile(FILE_PATH + file_name):
				# 第三次通讯：（防止粘包）
				#如果没有该文件，则发送准备好接收到服务端,开始接收(防止粘包)
				self.sockfd.send(("start|0").encode())
				new_size = 0  #设置文件初始大小为0
				M = hashlib.md5()       #生成md5对象
				#开始循环接受文件
				with open(FILE_PATH + file_name,'wb')as f:
					M = hashlib.md5() #生成md5对象
					while new_size < file_total_size:
					#防止粘包客户端最后一次判断还剩多少未接收，直接收剩下的，不再收		1024
						if file_total_size - new_size > 1024:  #要收不止一次
							size = 1024
						else:  #最后一次，剩多少收多少
							size = file_total_size - new_size
							# print("最后一次收:", size)
						data = self.sockfd.recv(size) #每次接受size文件
						new_size += len(data)  #在初始基础上累加
						#调用进度条模块的方法
						# progress.progress(self,new_size, file_total_size,50)
						def progerss(new_size, file_total_size):
							percent = float(new_size) / float(file_total_size)
							new_percent = percent * 100
							return new_percent		
						def progerss1():
							return progerss(new_size, file_total_size)
						temp = int(progerss1())
						if pgMemValue.value != temp:
							pgMemValue.value = temp
							print('hxw: pgMemValue.value = %d' % pgMemValue.value)

						M.update(data)
						f.write(data)  #写入文件
					else:
						print()
						print("文件下载成功!")
						new_file_md5 = M.hexdigest() #根据收到文件生成的md5
						print(new_size, file_total_size)
						f.close()
		
					receive_file_md5 = self.sockfd.recv(1024).decode() #	接原始文件的md5
					print("服务器 file md5:", receive_file_md5)
					print("客户端 file md5:", new_file_md5)
	
			else:	
				# msg = input("是否继续下载此文件:(y/n)")
				#如果本地存在此文件,将给服务端发送断点续传的请求标签
				#如果存在，则得到本地文件的大小，发送断点续传标识符，和本地文件大小到服务器，
				#以追加方式打开文件	
				native_size = os.path.getsize(FILE_PATH + file_name)
				#以追加方式写入文件
				with open(FILE_PATH + file_name,'ab')as f:
					M = hashlib.md5() #生成md5对象
					#得到本地已有文件的大小：
					# native_size = os.path.getsize(FILE_PATH + file_name)
					#发送本地文件大小和标识符到服务器
					self.sockfd.send(("Continue|%s"%native_size).encode())
					#开始继续接收文件
					new_size = native_size
					print(new_size)
	
					while native_size < file_total_size:
					#防止粘包客户端最后一次判断还剩多少未接收，直接收剩下的，不再收		1024
						if file_total_size - native_size > 1024:  #要收不止一次
							size = 1024
						else:  #最后一次，剩多少收多少
							size = file_total_size - native_size
							# print("最后一次收:", size)
						data = self.sockfd.recv(size) #每次接受size文件
						native_size += len(data)  #在初始基础上累加
						#调用进度条模块的方法
						# progress.progress(self,native_size, file_total_size,50)
						def progerss(new_size, file_total_size):
							percent = float(new_size) / float(file_total_size)
							new_percent = percent * 100
							return new_percent		
						def progerss1():
							return progerss(new_size, file_total_size)
						temp = int(progerss1())
						if pgMemValue.value != temp:
							pgMemValue.value = temp
							print('hxw: pgMemValue.value = %d' % pgMemValue.value)


						M.update(data)
						f.write(data)  #写入文件					
					else:
						# progress.progress(self,native_size, file_total_size,50)
						def progerss(new_size, file_total_size):
							percent = float(new_size) / float(file_total_size)
							new_percent = percent * 100
							return new_percent		
						def progerss1():
							return progerss(new_size, file_total_size)
						temp = int(progerss1())
						if pgMemValue.value != temp:
							pgMemValue.value = temp
							print('hxw: pgMemValue.value = %d' % pgMemValue.value)

						new_file_md5 = M.hexdigest() #根据收到文件生成的md5
						print("文件继续下载成功!")
						print(native_size, file_total_size)
						f.close()
					receive_file_md5 = self.sockfd.recv(1024).decode() #	接原始文件的md5
					print("服务器 file md5:", receive_file_md5)
					print("客户端 file md5:", new_file_md5)
	
		else:
			print("%s.哦豁，文件不存在" %file_exist)

	elif msg_d == "PUT_FOLDER": #开始接受文件夹
		self.sockfd.send("start_folder".encode()) #准被开始接受文见佳

		data = self.sockfd.recv(4096).decode()
		files = data.split('|')  #切割文件夹
		print("files==",files)
		#开始循环创建文件夹

		for folder in files:
			print("==",folder)
			try:
				os.makedirs(FILE_PATH + folder)
			except FileExistsError:
				pass
		else:
			print("文件夹创建完毕,开始接受文件")
			self.sockfd.send("start_file".encode())
		######

		while True:
			file_path = self.sockfd.recv(1024).decode() #收到文件名加路径和大小
			# print("文件名和大小",file_path)

			if file_path != "folder_succeed":
				fi = file_path.split(" ")
				file_name = fi[0]
				file_size = int(fi[1])
				print("文件名:",file_name, "大小",file_size)

				self.sockfd.send("准备好接受文件".encode())
	
				new_size = 0
				with open(FILE_PATH + file_name,'wb')as f:
					while new_size < file_size:
					#防止粘包客户端最后一次判断还剩多少未接收，直接收剩下的，不再收		1024
						if file_size - new_size > 1024:  #要收不止一次
							size = 1024
						else:  #最后一次，剩多少收多少
							size = file_size - new_size
							# print("最后一次收:", size)
						data = self.sockfd.recv(size) #每次接受size文件
						new_size += len(data)
						#调用进度条模块的方法
						# progress.progress(self,new_size, file_size,50)
						def progerss(new_size, file_size):
							percent = float(new_size) / float(file_size)
							new_percent = percent * 100
							return new_percent		
						def progerss1():
							return progerss(new_size, file_size)
						temp = int(progerss1())
						if pgMemValue.value != temp:
							pgMemValue.value = temp
							print('hxw: pgMemValue.value = %d' % pgMemValue.value)

						f.write(data)  #写入文件
					else:
						f.close()
						print("文件下载成功!")
						sleep(0.5)
						self.sockfd.send("OK".encode())

				# sleep(0.1)
				fileput = self.sockfd.recv(1024).decode() #每次接受size文件

				if fileput == "fileput_succeed":
					print("继续循环")
					continue


			else:

				print("文件夹接受完成")
				break

	else:
		print("Error")


def client_get(self, fileName, pgMemValue):
	p1 = Process(target = __client_get, args=(self, fileName, pgMemValue))
	p1.start()

	# p1.join()
	print('client get is running...')



