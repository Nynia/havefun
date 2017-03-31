# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import re
import os
import ftplib
import os
import socket


# import config
class MyFTP:
    def __init__(self, hostaddr, port, username, passwd, remotedir):
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

    def downloadFile(self):
        pass

    def uploadFiles(self, localpath, remotepath, targetname=''):
        self.ftp.cwd('/')
        self.changewd(remotepath)
        # url
        if re.match(r'^http://', localpath):
            r = requests.get(localpath)
            try:
                self.ftp.storbinary('STOR ' + targetname, r.content)
            except:
                print "upload failed1. check your permission."
        # local directory
        elif os.path.isdir(localpath):
            for file in os.listdir(localpath):
                src = os.path.join(localpath, file)
                print src
                if os.path.isfile(src):
                    try:
                        self.ftp.storbinary('STOR ' + file, open(src, 'rb'))
                    except:
                        print "upload failed. check your permission."
        # local file
        else:
            filename = localpath[localpath.rfind(os.sep) + 1:]
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
                self.ftp.mkd(dir[slash_pos + 1:])
                self.ftp.cwd(dir[slash_pos + 1:])
            else:
                self.ftp.mkd(dir)
                self.ftp.cwd(dir)


def update_comics(id_list):
    login_url = 'http://www.icartoons.cn/index.php?m=member&c=index&a=login'
    # login
    s = requests.Session()
    payload = {
        'username': '18118999630',
        'password': '1q2w3e4r',
        'dosubmit': '1'
    }
    r = s.post(login_url, data=payload)
    #print r.text
    myftp = MyFTP('192.168.114.138', 12345, 'jsgx', 'jsgx2017', '/')
    myftp.login()
    for i in range(len(id_list)):
        id = id_list[i]
        request_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=show&catid=25&id=%s' % id
        r = s.get(request_url)
        # check state
        match = re.search(u'状态：(&nbsp;)+(.*)<', r.text)
        if match:
            state = match.group(2)
            if state == u'已完结':
                print id, state
                # return
        else:
            print id
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        for ss in soup.find_all(id=re.compile("positive_setinfo_*")):
            for a_tag in ss.find_all('a'):
                content = a_tag.get_text()
                if re.search(u'第\d+集', content):
                    episode = re.search(u'第(\d+)集', content).group(1)
                    provisionid = re.search(u'provisionid=(\d+)', unicode(a_tag)).group(1)
                    # print episode, provisionid
                    img_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=play_comic&id=%s&provisionid=%s' % (
                        id, provisionid)
                    r = s.get(img_url)
                    img_soup = BeautifulSoup(r.text, 'html.parser')
                    for img_tag in img_soup.find_all('img'):
                        if img_tag.has_attr('id'):
                            #print i,id,episode,img_tag['id']
                            if len(img_tag['src']) < 30:
                                continue
                            seq = img_tag['id'][3:]
                            if len(seq) == 1:
                                seq = '0'+seq
                            print i, id, episode, seq
                            # download pics
                            # myftp.changewd('comic/20082903/123')
                            myftp.uploadFiles(img_tag['src'], '/comics/' + id + '/' + episode, img_tag['id'][3:] + '.jpg')
                            # with open(target_path, 'wb') as handle:
                            #    response = requests.get(img_tag['src'], stream=True)
                            #    for block in response.iter_content(1024):
                            #        if not block:
                            #            break
                            #        handle.write(block)
                            # upload_qiniu(target_path, target_name)

id_list = ['200103359', '200103364', '200103379', '200103383', '200103388', '200103408', '200103424', '200103454',
           '200103457', '200103377', '200103380', '200103382', '200103386', '200103391', '200103393', '200103394',
           '200103396', '200103398', '200103401', '200103403', '200103405']
update_comics(id_list)
