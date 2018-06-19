#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from multiprocessing import Event,Process
from progress import *
from time import sleep
from conf import PATH_
import os,json
import re
import socket

FILE_PATH = PATH_

def __client_get(self, fileName, pgMemValue):
	cmd_split = fileName.split()
	file_name = cmd_split[1]
	msg_dic={
			"directive": "get",
			"file_name": file_name
			}

	print("dic",msg_dic)
	#第一次通讯：发送标识符,文件名到服务器
	self.client.send(json.dumps(msg_dic).encode())
	#收到服务器发送文件标识
	msg_d = self.client.recv(1024).decode()
	print(msg_d)
	#判断收到服务器开始发送文件开始文件夹
	if msg_d == "PUT_FILE":
		data = self.client.recv(1024).decode()
		server_response = data.split('|')
		file_all_size = int(server_response[0])  #文件总大小
		file_pa = server_response[1].split('/')[-1]
		print(file_pa)

		#通过判断本地是否有此文件，来确认是否启用断点续传
		if not os.path.isfile(FILE_PATH + file_pa):
			#如果没有该文件，则发送准备好接收到服务端,开始接收(防止粘包)
			self.client.send(("start|0").encode())
			new_size = 0 #设置文件初始大小为0
			f = open(FILE_PATH + file_pa,'wb')
			#循环接受文件
			while new_size < file_all_size:
				if file_all_size - new_size > 1024:
					size = 1024
				else:
					size = file_all_size - new_size
				data = self.client.recv(size)
				new_size += len(data)
				# progres(new_size,file_all_size)
				#--------------------------------------------
				def progerss(new_size, file_all_size):
					try:
						percent = float(new_size) / float(file_all_size)
						new_percent = percent * 100
					except ZeroDivisionError:
						new_percent = 0.01
					return new_percent		
				def progerss1():
					return progerss(new_size, file_all_size)
				temp = int(progerss1())
				if pgMemValue.value != temp:
					pgMemValue.value = temp
					print('hxw: pgMemValue.value = %d' % pgMemValue.value)				
				#--------------------------------------------
				f.write(data)  #写入文件
			else:
				print("文件下载成功!")
				f.close()

		else:  #本地存在该文件,继续接受,断点续传
			#如果存在，则得到本地文件的大小，发送断点续传标识符，和本地文件大小到服务器，
			native_size = os.path.getsize(FILE_PATH + file_pa)
			#发送本地文件大小和标识符到服务器
			self.client.send(("Continue|%s"%native_size).encode())
			#开始继续接收文件,以追加方式写入文件
			f = open(FILE_PATH + file_pa,'ab')		
			while native_size < file_all_size:
				if file_all_size - native_size > 1024:
					size = 1024
				else:
					size = file_all_size - native_size
				data = self.client.recv(size)
				native_size += len(data)
				# progres(native_size,file_all_size)
				#--------------------------------------------
				def progerss(new_size, file_all_size):
					try:
						percent = float(new_size) / float(file_all_size)
						new_percent = percent * 100
					except ZeroDivisionError:
						new_percent = 0.01
					return new_percent	
				def progerss1():
					return progerss(new_size, file_all_size)
				temp = int(progerss1())
				if pgMemValue.value != temp:
					pgMemValue.value = temp
					print('hxw: pgMemValue.value = %d' % pgMemValue.value)				
				#--------------------------------------------				
				f.write(data)  #写入文件
			else:
				print("文件下载成功!")
				f.close()

	elif msg_d == "PUT_FOLDER":
		self.client.send(("start_folder".encode()))
		floder = json.loads(self.client.recv(4096).decode())
		print("=======",floder)
		for i in floder:
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
			except UnboundLocalError:
				os.makedirs(FILE_PATH + file_name)
				if os.path.exists(FILE_PATH + file_name):
					print("文件夹创建完毕,开始接受文件")
				else:
					print("Error,")

		self.client.send(("start_file".encode()))
		while True:
			file_ = self.client.recv(2048).decode()
			if file_ != "allfile_succee":
				fi = file_.split(" ")
				filename = fi[0]
				file_size = int(fi[1])
				print("文件名:",filename, "大小",file_size)
				self.client.send(("start_succeed".encode()))
				f_size = 0
				f = open(FILE_PATH + filename,'wb')
				while f_size < file_size:
					if file_size - f_size > 1024:  #要收不止一次
						size = 1024
					else:  #最后一次，剩多少收多少
						size = file_size - f_size
					data = self.client.recv(size) #每次接受size文件
					f_size += len(data)				
					# progres(f_size,file_size)
				#--------------------------------------------
				def progerss(f_size, file_size):
					try:
						percent = float(f_size) / float(file_size)
						new_percent = percent * 100
					except ZeroDivisionError:
						new_percent = 0.01
					return new_percent		
				def progerss1():
					return progerss(f_size, file_size)
				temp = int(progerss1())
				if pgMemValue.value != temp:
					pgMemValue.value = temp
					print('hxw: pgMemValue.value = %d' % pgMemValue.value)				
				#--------------------------------------------					
					f.write(data)  #写入文件
				else:
					f.close()
					print("文件下载成功!")
				sleep(0.2)
				self.client.send(("start_file_succeed".encode()))
				file_ok = self.client.recv(1024).decode()
				if file_ok == "succee":
					print("继续循环")
					continue
			else:
				print("文件夹接受完成")
				break
	else:
		print("服务器文件不存在")
		

def do_get(self, fileName, pgMemValue):
	p1 = Process(target = __client_get, args=(self, fileName, pgMemValue))
	p1.start()

	# p1.join()
	print('client get is running...')