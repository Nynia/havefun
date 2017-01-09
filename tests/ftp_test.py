#!/usr/bin/python
# -*- coding: utf-8 -*-
import ftplib
import os
import socket
from app.utils.ftp import MyFTP
HOST = '202.102.41.224'
TIMEOUT = 30
USERNAME = 'admin'
PASSWD = 'admin123'
DIRN = 'test/util'
FILE = 'AmountUtils.java'
def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror):
        print 'ERROR:cannot reach " %s"' % HOST
        return
    print '***Connected to host "%s"' % HOST

    try:
        f.login(USERNAME, PASSWD)
    except ftplib.error_perm:
        print 'ERROR: cannot login'
        f.quit()
        return
    print '*** Logged in as %s' % USERNAME
    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print 'ERRORL cannot CD to "%s"' % DIRN
        f.quit()
        return
    print '*** Changed to "%s" folder' % DIRN
    try:
        #传一个回调函数给retrbinary() 它在每接收一个二进制数据时都会被调用
        file = open(FILE, 'wb')
        f.retrbinary('RETR %s' % FILE, file.write)
    except ftplib.error_perm:
        print 'ERROR: cannot read file "%s"' % FILE
        os.unlink(FILE)
    else:
        print '*** Downloaded "%s" to CWD' % FILE
    f.quit()
    return
if __name__ == '__main__':
    #main()
    myftp = MyFTP('202.102.41.224',21,'admin','admin123','.')
    myftp.login()
    #myftp.changewd('comic/20082903/123')
    myftp.uploadFiles('D:\\comic\\1\\3434343\\haowan.html', 'comic/1/3434343')