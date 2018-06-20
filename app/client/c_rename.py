#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os,json

def do_crename(self, *args):
	cmd_split = args[0].split()
	filename = cmd_split[1]
	new_filename = cmd_split[2]
	msg_dic={
			"directive": "rename",
			"file_name": filename,
			"new_filename": new_filename
			}
	#发送要创建的目录名和操作指令
	self.client.send(json.dumps(msg_dic).encode())

	data = self.client.recv(1024).decode()

	if data == "file_rename_succeed":
		# print("重命名成功")
		return True
	elif data == "file_rename_defeated":
		# print("重命名失败，请检查")
		return False
	elif data == "file_name_exist":
		# print("该名字文件以存在！")
		return "该名字文件以存在！"
