#!/usr/bin/python3
import os,sys
import json
import hashlib
from core import folder_size

FILE_PATH = "/tmp/server_data/"
def server_deal_put(self, *args):
	#第一次通讯，的到客户端文件，文件大小
	# 处理客户端上传文件的请求
	cmd_split = args[0].split()
	file_name = cmd_split[1]  #需要上传的文件
	file_total_size = int(cmd_split[2])  #得到文件总大小

	# 用户家目录总大小
	HONE_MAX_SIZE = 10240000000
	#当前家目录磁盘空间大小
	dir_size = folder_size.getdirsize(FILE_PATH)
	print("当前用户磁盘空间大小:%s" % dir_size)
	#如果用户家目录下的大小加上本次将上传文件的大小仍小于最大的磁盘配额，则可以继续上传
	file_exist = 200 
	size_sum = dir_size + file_total_size
	print(size_sum)

	if size_sum < HONE_MAX_SIZE:
		#服务器判断用户家目录下面有没有这个文件和否是一个文件,来确认是否启用断点续传
		if not os.path.isfile(FILE_PATH + file_name):
			# 如果没有该文件，则发送准备好接收到服务端,开始接收(防止粘包)
			self.connfd.send(("start|0").encode())
			new_size = 0  #设置文件初始大小为0
			M = hashlib.md5()       #生成md5对象
			#开始循环接受文件
			with open(FILE_PATH + file_name,'wb') as f:
				while new_size < file_total_size:
					if file_total_size - new_size > 1024:  #要收不止一次
						size = 1024
					else:  #最后一次，剩多少收多少
						size = file_total_size - new_size
						# print("最后一次收:", size)
					data = self.connfd.recv(size) #每次接受size文件
					new_size += len(data)  #在初始基础上累加
					M.update(data)
					f.write(data)  #写入文件

				else:
					print()
					print("文件上传成功!")
					print(new_size, file_total_size)
					f.close()
					self.connfd.send(M.hexdigest().encode())					

		else:
			#如果本地存在此文件,将给服务端发送断点续传的请求标签
			#如果存在，则得到本地文件的大小，发送断点续传标识符，和本地文件大小到服务器，
			#以追加方式打开文件	
			native_size = os.path.getsize(FILE_PATH + file_name)
			print('----->>',native_size)
				# 以追加的方式写文件
			with open(FILE_PATH + file_name,'ab') as f:
				M = hashlib.md5() #生成md5对象
				#得到服务器已有文件的大小：
				#发送本地文件大小和标识符到服务器
				self.connfd.send(("Continue|%s"%native_size).encode())
				#开始继续接收文件
				new_size = native_size
				print('------')
				print(new_size)

				while native_size < file_total_size:
				#防止粘包客户端最后一次判断还剩多少未接收，直接收剩下的，不再收		1024
					if file_total_size - native_size > 1024:  #要收不止一次
						size = 1024
					else:  #最后一次，剩多少收多少
						size = file_total_size - native_size
						# print("最后一次收:", size)
					data = self.connfd.recv(size) #每次接受size文件
					native_size += len(data)  #在初始基础上累加
					M.update(data)
					f.write(data)  #写入文件					
				else:
					print()
					new_file_md5 = M.hexdigest() #根据收到文件生成的md5
					print("文件继续上传成功!")
					print(native_size, file_total_size)
					f.close()
					self.connfd.send(M.hexdigest().encode())

	else:
		Home_size = '402'  #家目录磁盘空间不足!
		self.connfd.send(("%s|0"%Home_size).encode())




