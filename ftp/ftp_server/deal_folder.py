#!/usr/bin/python3

from time import sleep
import time
import os,sys
import re



FILE_PATH = "/tmp/server_data/"

def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)

def file_max(filename):
        filesize = os.stat(FILE_PATH + folder_name + "/" + filename).st_size
        file_size = humanbytes(filesize)
        return file_size


def file_form(filename):
    if not os.path.isdir(FILE_PATH + folder_name + "/" + filename):
        ext = re.findall(".tar.gz","%s"%filename)
        if ext == []:
            #文件类型:
            File = os.path.splitext(filename)
            file_ext = File[1]
            print(file_ext)

        else:
            file_ext = ext[0]

        return file_ext
    else:
        file_ext = "folder"
        return file_ext

def file_date(filename):
    print("==",FILE_PATH + folder_name + "/" + filename)
    a = os.path.getmtime(FILE_PATH + folder_name + "/"+ filename)
    b = time.localtime(a)

    d = "%s-%s-%s %s:%s"%(b[0],b[1],b[2],b[3],b[4])
    return d

def server_deal_folder(self, *args):
    #第一次通讯，收到客户端发来的标识码和目录名：
    cmd_split = args[0].split('|')
    global folder_name
    folder_name = cmd_split[1]  #得到目录名

    print("+++",folder_name)

    # Filelist = os.listdir(FOLDER_PATH)
    Filelist = os.listdir(FILE_PATH + folder_name)
    # print("folder====",Filelist)
    if not Filelist:
        self.connfd.send("Filelist_no_exit".encode())
        return
    else:
        self.connfd.send("Filelist_exit".encode())
    sleep(0.01)  #防止粘包
    files = ""
    for filename in Filelist:
        if filename.startswith('.'):
            continue
        file_all = "%s %s %s %s"%(filename, file_form(filename), file_date(filename), file_max(filename))
        files += file_all + '|'
        # files += filename + '|'
    print("===",files)

    self.connfd.send(files.encode())    