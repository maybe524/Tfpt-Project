#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#客户端
import socket
import hashlib
import os
import json
import socket
from list_ import do_ls
from rm import do_rm
from cd import do_cd
from get import do_get
from put import do_put
from mkdir import do_mkdir
from rename import do_rename

class FtpClient:
	def __init__(self):
		self.client = socket.socket()

	def connect(self, ip, port):
		self.client.connect((ip, port))

	# def interactive(self):
	# 	while True:
	# 		msg_ = input("请输入操作>>>").strip()
	# 		if len(msg_) == 0 or len(msg_.split(" ")) < 2:
	# 			print("输出有误！！！")
	# 			continue
	# 		msg = msg_.split(" ")
	# 		if hasattr(self, msg[0]):
	# 			func = getattr(self, msg[0])
	# 			func(msg_)


	def list_(self):
		return do_ls(self)

	def cd(self,fileName):
		return do_cd(self, fileName)

	def get(self, fileName, pgMemValue):
		return do_get(self, fileName, pgMemValue)

	def put(self, fileName, pgbarChange):
		return do_put(self, fileName, pgbarChange)

	def mkdir(self, *args):
		return do_mkdir(self, *args)

	def rename(self, *args):
		return do_rename(self, *args)

	def rm(self, *args):
		return do_rm(self, *args)


# if __name__ == "__main__":
# 	ftp_client = FtpClient()
# 	ftp_client.connect("127.0.0.1",8889)
# 	ftp_client.list_()
# 	ftp_client.interactive()

