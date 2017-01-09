from app import config
import ftplib
import os
import socket

class MyFTP:
    def __init__(self,hostaddr,port,username,passwd,remotedir):
        self.ftp = ftplib.FTP()
        self.hostaddr = hostaddr
        self.username = username
        self.passwd = passwd
        self.port = port
        self.remotedir = remotedir
    def __del__(self):
        self.ftp.close()
    # login
    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            ftp.connect(self.hostaddr, self.port)
            print 'connected to %s' % (self.hostaddr)
            ftp.login(self.username, self.passwd)
            print 'login as %s' % (self.username)
        except Exception:
            print 'connect or login error'
        try:
            ftp.cwd(self.remotedir)
            print 'change dir to %s' % self.remotedir
        except Exception:
            print 'change dir error'

    def downloadFile(self):
        pass
    def uploadFiles(self, localpath, remotepath):
        self.changewd(remotepath)
        if os.path.isdir(localpath):
            for file in os.listdir(localpath):
                src = os.path.join(localpath, file)
                print src
                if os.path.isfile(src):
                    try:
                        self.ftp.storbinary('STOR ' + file, open(src, 'rb'))
                    except:
                        print "upload failed. check your permission."
        else:
            filename = localpath[localpath.rfind(os.sep)+1:]
            print filename
            try:
                self.ftp.storbinary('STOR ' + filename, open(localpath, 'rb'))
            except:
                print "upload failed. check your permission."
    def changewd(self, dir):
        try:
            self.ftp.cwd(dir)
        except ftplib.error_perm:
            slash_pos = dir.rfind('/')
            if slash_pos != -1:
                self.changewd(dir[:slash_pos])
                self.ftp.mkd(dir[slash_pos+1:])
                self.ftp.cwd(dir[slash_pos+1:])
            else:
                self.ftp.mkd(dir)
                self.ftp.cwd(dir)