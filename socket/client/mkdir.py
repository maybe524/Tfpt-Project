#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os,json

def do_mkdir(self, *args):
	cmd_split = args[0].split()
	filename = cmd_split[1]
	msg_dic={
			"directive": "mkdir",
			"file_name": filename
			}
	#发送要创建的目录名和操作指令	
	self.client.send(json.dumps(msg_dic).encode())
	#收到服务端消息
	data = self.client.recv(1024).decode()
	if data == "creation_folder_succeed":
		print("目录创建成功")
	elif data == "creation_folder_defeated":
		print("目录创建失败，请检查")
	elif data == "folder_exist":
		print("目录以存在")
