#!/usr/bin/python3
import os,sys
import socket
import hashlib
import json
import re
from time import *

FILE_PATH = "/tmp/server_data/"

#处理客户端下载文件的请求
# 服务器收到文件和标识符，调用get方法
def server_deal_get(self, *args):
	'''
	filename = args[1] #文件
	'''
	#第一次通讯，收到客户端发来的标识码和文件名：
	cmd_split = args[0].split('|')
	file_name = cmd_split[1]  #得到文件名
	print("file_name",file_name)
	#判断是否是文件夹
	if not os.path.isdir(FILE_PATH + file_name):
		#如果是一个文件,发送文件表示到客户端
		self.connfd.send("PUT_FILE".encode())
		client_response = self.connfd.recv(1024).decode()
	#服务器判断用户家目录下面有没有这个文件和否是一个文件
		print("===",FILE_PATH + file_name)
		if os.path.isfile(FILE_PATH + file_name):

			#如果有这个文件：得到文件总大小
			file_size = os.stat(FILE_PATH + file_name).st_size
			#生成md5对象
			M = hashlib.md5()
			#给文件存在一个标示码,发送到客户端
			file_exist = 200  
			#第二次通讯，发送文件总大小，和文件存不存在标识码到客户端路径的的阿斯顿发生地方
			msg_dic = "%s|%s"%(file_size,file_exist)
			self.connfd.send(msg_dic.encode())
	
			#第三次通讯：确定客户端信息，判断是直接发送还是断点续传
			client_response = self.connfd.recv(1024).decode()
			#得到客户端发来标识符，判断是否执行断点续传
			client_tag = client_response.split('|')[0]
			#得到客户端文件大小
			client_file_size = int(client_response.split('|')[1])
	
			#打开文件
			with open(FILE_PATH + file_name,'rb')as f:
				##判断是否准备好,如果是start，这开始从头发送文件，
				if client_tag == "start": 
					new_size = 0  #设置文件初始大小为0 
					#开始循环发送文件
					for line in f:
						self.connfd.send(line)
						M.update(line)
						new_size += len(line)
					else:
						print("文件上传至客户成功！")
					f.close() #关闭文件
					self.connfd.send(M.hexdigest().encode())  #发送md5
	
				elif client_tag == "Continue":
					
					#使用seek方法来实现将文件指针放在上次断点处，并继续传输，进而完成断点续传的功能，第一个参数表示指针偏移位数，第二个参数表示，从文件开头开偏移
					# 使用seek方法来实现将文件指针重置
					new_size = client_file_size
					print(new_size)
	
					f.seek(new_size,0)
					for line in f:  #循环继续发送
						self.connfd.send(line)
						M.update(line)
						new_size += len(line)
						# if new_size >= file_size:break
					else:
						print("文件继续上传至客户成功！")
					f.close()	
					self.connfd.send(M.hexdigest().encode())  #发送md5
	
		else:
			file_exist = 404
			msg_dic = "0|%s"%file_exist
			self.connfd.send(msg_dic.encode())

	else: 
		#如果是一个目录
		# print("yes66666666",file_name)
		fil = []  #目录
		filepath = FILE_PATH + file_name
		def gci_folder(filepath):  
		#遍历file_name下所有文件，包括子目录  
			files = os.listdir(filepath)
			for fi in files:  
				fi_d = os.path.join(filepath,fi)
				# print("000",fi_d)
				if os.path.isdir(fi_d): 
					gci_folder(fi_d)
					# print("folde==",fi_d)  #得到所有目录
					y = "".join(re.findall("%s\S+"%file_name,fi_d))
					fil.append(y)
					# print("==",fi_d)
					# fil += fi_d + '|'


		gci_folder(filepath)
		# print("===",fil)
		f_name = "|".join(fil)
		# print("123",f_name)
		
		
		file = []  #文件
		def gci(filepath):  
			#遍历file_name下所有文件，包括子目录  
			files = os.listdir(filepath) 
			print("nnnnn",files)
			for fi in files:  
				fi_d = os.path.join(filepath,fi)  
				if os.path.isdir(fi_d):  
					gci(fi_d)
				else:
					f_name = os.path.join(filepath,fi_d) #得到所有文件
					y = "".join(re.findall("%s\S+"%file_name,f_name))
					file_size = os.stat(f_name).st_size  #得到文件大小
					file.append("%s %s"%(y,file_size))
					# file  += fi_d + " " + file_size + '|'
		

		gci(filepath)
		x = "|".join(file)
		# print("222",x)

		得到得到文件的dd的啊的哦目录#+++++++++++++++发送put_folde到服务器,开始传输文件夹
		self.connfd.send("PUT_FOLDER".encode())
		#判断是否准备好,如果是start，这开始发送文件夹，
		client_folder = self.connfd.recv(1024).decode()

		if client_folder == "start_folder":
			self.connfd.send(f_name.encode())

		client_file = self.connfd.recv(1024).decode()

		if client_file == "start_file":
			#开始循环发送文件
			files = x.split('|')
			for fil in files:
				sleep(0.5)
				self.connfd.send(fil.encode())  #发送文件路径和文件大小
				clien = self.connfd.recv(1024).decode() #客户段准备好,开始发送文件
				fi = fil.split(" ")[0]
				with open(FILE_PATH + fi,'rb')as f:  #打开文件
					# new_size = 0  #设置文件初始大小为0 
					#开始循环发送文件
					for line in f:
						self.connfd.send(line)

					else:
						sleep(0.1)
						f.close() #关闭文件
					fiel_ok = self.connfd.recv(1024).decode()
					print(fiel_ok)

					self.connfd.send("fileput_succeed".encode())
					sleep(0.5)
			else:
				self.connfd.send("folder_succeed".encode())

