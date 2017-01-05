# 例：FTP编程
from ftplib import FTP

ftp = FTP()
timeout = 30
port = 9250
ftp.connect('61.160.185.52', port, timeout)  # 连接FTP服务器
ftp.login('admin', 'admin')  # 登录
print ftp.getwelcome()  # 获得欢迎信息
ftp.cwd('file/test')  # 设置FTP路径
list = ftp.nlst()  # 获得目录列表
for name in list:
    print(name)  # 打印文件名字
path = 'd:/data/' + name  # 文件保存路径
f = open(path, 'wb')  # 打开要保存文件
filename = 'RETR ' + name  # 保存FTP文件
ftp.retrbinary(filename, f.write)  # 保存FTP上的文件
ftp.delete(name)  # 删除FTP文件
ftp.storbinary('STOR ' + filename, open(path, 'rb'))  # 上传FTP文件
ftp.quit()  # 退出FTP服务器
