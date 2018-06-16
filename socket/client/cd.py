#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os,json
import re

def do_cd(self, fileName):
	cmd_split = fileName.split()
	global filename
	filename = cmd_split[1]
	print("==",filename)
	msg_dic={
			"directive": "cd",
			"file_name": filename
			}
	#发送目录名和操作指令
	self.client.send(json.dumps(msg_dic).encode())

	data = self.client.recv(1024).decode()
	L = []
	if data == 'Filelist_exit':
		#得到服务器家目录所有目录
		all_folder = json.loads(self.client.recv(2048).decode())

		for file in all_folder:
			file_name = file.split(' ')
			FILE_NAME = (file_name[0]).split('/')[-1]
			FILE_EXT = file_name[1]
			FILE_DATE = file_name[2]+' '+file_name[3]
			FILE_SIZE = file_name[4]+' '+file_name[5]

			L.append([FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE])
			print(FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE)
		return L
	# 		# print(file)
	else:
		print("请求文件列表失败")
