# -*-coding:utf-8-*-
from app.utils.ftp import MyFTP
from app.models import Comic,ComicChapterInfo
import datetime
from app import db

myftp = MyFTP('192.168.114.138', 12345, 'jsgx', 'jsgx2017', '/')
myftp.login()

id_list = ['200103359', '200103364', '200103379', '200103383', '200103388', '200103408', '200103424', '200103454',
           '200103457', '200103377', '200103380', '200103382', '200103386', '200103391', '200103393', '200103394',
           '200103396', '200103398', '200103401', '200103403', '200103405']

for id in id_list:
    comic = Comic.query.get(int(id))
    for chapter in comic.curchapter:
        filelist = myftp.listfiles('/comics' + '/' + id + '/' + chapter)
        quantity = len(filelist)
        chapterinfo = ComicChapterInfo()
        chapterinfo.bookid = id
        chapterinfo.chapterid = chapter
        chapterinfo.quantity = quantity

        chapterinfo.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        chapterinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

        db.session.add(chapterinfo)
        db.session.commit()