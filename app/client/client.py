#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#客户端
import socket
import hashlib
import os
import json
import socket

from c_list import do_cls
from c_rm import do_crm
from c_cd import do_ccd
from c_get import do_cget
from c_put import do_cput
from c_mkdir import do_cmkdir
from c_rename import do_crename
from c_login import do_clogin
from c_register import do_cregister

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


	def list(self):
		return do_cls(self)

	def cd(self,fileName):
		return do_ccd(self, fileName)

	def get(self, fileName, pgMemValue):
		return do_cget(self, fileName, pgMemValue)

	def put(self, fileName, pgbarChange):
		return do_cput(self, fileName, pgbarChange)

	def mkdir(self, *args):
		return do_cmkdir(self, *args)

	def rename(self, *args):
		return do_crename(self, *args)

	def rm(self, *args):
		return do_crm(self, *args)

	def login(self, *args):
		return do_clogin(self, *args)

	def register(self, *args):
		return do_cregister(self, *args)


# if __name__ == "__main__":
# 	ftp_client = FtpClient()
# 	ftp_client.connect("127.0.0.1",8889)
# 	ftp_client.list_()
# 	ftp_client.interactive()

