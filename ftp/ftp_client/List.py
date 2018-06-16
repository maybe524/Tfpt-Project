#!/usr/bin/python3

import os,sys

L = []
#显示功能
def client_list(self):
		
		self.sockfd.send('LIST'.encode()) #发送请求类别
		#服务器回复 Filelist_no_exit / Filelist_exit
		data = self.sockfd.recv(1024).decode()

		if data == 'Filelist_exit':
			data = self.sockfd.recv(4096).decode()
			files = data.split('|')
			files.remove('')

			

			for file in files:
				file_name = file.split(' ')

				FILE_NAME = file_name[0]
				FILE_EXT = file_name[1]
				FILE_DATE = file_name[2]+' '+file_name[3]
				FILE_SIZE = file_name[4]+' '+file_name[5]
				global L

				L.append([FILE_NAME, FILE_SIZE, FILE_EXT, FILE_DATE])
				# return (FILE_NAME, FILE_EXT, FILE_DATE, FILE_SIZE)
			return L

			# print("文件列表展示完毕")
		else:
			print("请求文件列表失败")
