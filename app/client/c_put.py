#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from progress import *
from multiprocessing import Event,Process
import socket
import os
import json
import re
from time import sleep
from progress import *
from c_conf import PATH_

FILE_PATH = PATH_


def __client_put(self, fileName, pgbarChange):
	cmd_split = fileName.split()
	filename = cmd_split[1]
	# data = self.client.recv(1024)
	# print("recv:>",data.decode())
    # 判断用户本地上传目录下面有没有这个文件
	if os.path.exists(FILE_PATH + filename):
#-----------------------------------------------------------------------
		# 判断是否是文件夹
		if not os.path.isdir(FILE_PATH + filename):
			# 如果有这个文件：得到文件总大小
			file_size = os.stat(FILE_PATH + filename).st_size
			msg_dic = {
					"directive": "put",
					"file_name": filename,
					"file_size": file_size,
					"file_type": "FILE"
					}
			# 第一次通讯，发送操作指令，文件，文件大小
			self.client.send(json.dumps(msg_dic).encode())
			file_ = self.client.recv(1024).decode()
			client_put = file_.split('|')[0]
			server_file_size = int(file_.split('|')[1])
			# 打开文件
			f = open(FILE_PATH + filename, 'rb')
			if client_put == "Start":
				# 开始循环发送文件
				for line in f:
					self.client.send(line)
					send_size = f.tell()
					progres(send_size, file_size)
				else:
					f.close()
					print("file upload success")

			elif client_put == "Continue":
				new_size = server_file_size
				f.seek(new_size, 0)
				# 开始循环发送文件
				for line in f:
					self.client.send(line)
					new_size += len(line)
					progres(new_size, file_size)
				else:
					f.close()
					print("file upload success")

			elif client_put == "Home_size":
				print("家目录磁盘空间不足!")

		else:  # 文件夹
			# 发送put_folde到服务器,开始传输文件夹
			msg_dic = {
					"directive": "put",
					"file_name": filename,
					"file_size": 0,
					"file_type": "FOLDER"
					}
			self.client.send(json.dumps(msg_dic).encode())
			File_pa = []
			File = []
			def folder(FILE_PATH):
            # 遍历file_name下所有文件，包括子目录
				files = os.listdir(FILE_PATH)
				for fi in files:
					fi_d = os.path.join(FILE_PATH, fi)
					if os.path.isdir(fi_d):
						folder(fi_d)
						fi_ = "".join(re.findall("%s\S+" % filename, fi_d))
						File_pa.append(fi_)  # 得到所有目录
					else:
						f_name = os.path.join(FILE_PATH, fi_d)  # 得到所有文件
						fi_f = "".join(re.findall("%s\S+" % filename, f_name))
						File.append(fi_f)

			folder(FILE_PATH)
			for i in range(len(File)-1,-1,-1):
				if File[i] == '':
					File.remove('')
			for i in range(len(File_pa)-1,-1,-1):
				if File_pa[i] == '':
					File_pa.remove('')
#--------------------------------------------------
			folder = self.client.recv(1024).decode()
			# 发送所有文件夹
			if folder == "start_folder":
				self.client.send(json.dumps(File_pa).encode())
			#发送所有文件
			folder = self.client.recv(1024).decode()
			if folder == "start_file":
				print("上传文件")
				for f in File:
					file_size = os.stat(FILE_PATH + f).st_size  #得到文件大小
					f_s = "%s %s"%(f,file_size)
					self.client.send(f_s.encode())
					client_ = self.client.recv(1024).decode()
					fi = f.split(" ")[0]
					f = open(FILE_PATH + fi, 'rb')
					for line in f:
						self.client.send(line)
						send_size = f.tell()
						progres(send_size, file_size)						
					else:
						f.close()
					file_ok = self.client.recv(1024).decode()
					print(file_ok)
					sleep(0.2)
					self.client.send("succee".encode())
				else:
					sleep(0.3)
					self.client.send("allfile_succee".encode())
	else:
		print("文件不存在")

def do_cput(self, fileName, pgbarChange):
	p1 = Process(target = __client_put, args=(self, fileName, pgbarChange))
	p1.start()

	# p1.join()
	print('client put is running...')