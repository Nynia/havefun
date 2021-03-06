# -*-coding:utf-8-*-
import re,requests,os,ftplib,socket,json

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
            timeout = 30
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
    def listfiles(self, dirname):
        return self.ftp.nlst(dirname)
    def downloadFile(self):
        pass
    def uploadFiles(self, localpath, remotepath, targetname=''):
        self.ftp.cwd('/')
        self.changewd(remotepath)
        #url
        if re.match(r'^http://', localpath):
            r = requests.get(localpath)
            try:
                self.ftp.storbinary('STOR ' + targetname, r.content)
            except:
                print "upload failed. check your permission."
        #local directory
        elif os.path.isdir(localpath):
            for file in os.listdir(localpath):
                src = os.path.join(localpath, file)
                print src
                if os.path.isfile(src):
                    try:
                        self.ftp.storbinary('STOR ' + file, open(src, 'rb'))
                    except:
                        print "upload failed. check your permission."
        #local file
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

myftp = MyFTP('192.168.114.138', 12345, 'jsgx', 'jsgx2017', '/')
myftp.login()

id_list = ['200103359', '200103364', '200103379', '200103383', '200103388', '200103408', '200103424', '200103454',
           '200103457', '200103377', '200103380', '200103382', '200103386', '200103391', '200103393', '200103394',
           '200103396', '200103398', '200103401', '200103403', '200103405']

base_url = 'http://127.0.0.1:5000/api/v1.0/comics'
for id in id_list:
    url = base_url + '/' + id
    r = requests.get(url)
    print r.text
    json_result = json.loads(r.text)
    data = json_result['data']
    curchapter = data['curchapter']
    print curchapter
    for chapter in range(int(curchapter)):
        filelist = myftp.listfiles('/comics' + '/' + id + '/' + str(chapter+1))
        quantity = len(filelist)
        url = base_url + '/chapters/' + id
        data = {
            'chapterid':chapter+1,
            'quantity':quantity
        }
        r = requests.post(url,data=data)
        print r.text