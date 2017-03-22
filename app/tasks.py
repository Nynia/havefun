# -*-coding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup
from app.utils.ftp import MyFTP
import base64
import json
from app import db


def comic_job():
    # get all comics from database
    base_url = 'http://127.0.0.1:5000/api/v1.0/comics'
    r = requests.get(base_url)
    json_result = r.json()

    # ftp init
    # myftp = MyFTP('202.102.41.224', 21, 'admin', 'admin123', '.')
    # myftp.login()

    # log in
    login_url = 'http://www.icartoons.cn/index.php?m=member&c=index&a=login'
    s = requests.Session()
    payload = {
        'username': '18118999630',
        'password': '1q2w3e4r',
        'dosubmit': '1'
    }
    r = s.post(login_url, data=payload)
    #
    if json_result['code'] == '0':
        data = json_result['data']
        for item in data:
            id = item['id']
            name = item['comicname']
            local_state = item['state']
            local_chapter = item['curchapter']
            remote_state = '0'
            remote_chapter = 0

            print 'update %s...' % name
            if local_state == '1':
                continue
            else:
                # requests
                request_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=show&catid=25&id=%s' % id
                r = s.get(request_url)
                # check state
                match = re.search(u'状态：(&nbsp;)+(.*)<', r.text)
                if match:
                    state = match.group(2)
                    if state == u'已完结':
                        remote_state = '1'
                # parse
                soup = BeautifulSoup(r.text, 'html.parser')
                # info

                for a_tag in soup.find_all('a'):
                    content = a_tag.get_text()
                    if re.search(u'第\d+集', content):
                        episode = re.search(u'第(\d+)集', content).group(1)
                        if int(episode) > remote_chapter:
                            remote_chapter = int(episode)
                        # update episode
                        if int(episode) > local_chapter:
                            print 'add chapter %s' % episode
                            provisionid = re.search(u'provisionid=(\d+)', unicode(a_tag)).group(1)
                            img_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=play_comic&id=%s&provisionid=%s' % (
                                id, provisionid)
                            r = s.get(img_url)
                            img_soup = BeautifulSoup(r.text, 'html.parser')
                            for img_tag in img_soup.find_all('img'):
                                if img_tag.has_attr('id'):
                                    print img_tag['id'], img_tag['src']
                                    if len(img_tag['src']) < 30:
                                        continue
                                        # myftp.uploadFiles(img_tag['src'], 'comics/' + id + '/' + episode,
                                        #                  img_tag['id'][3:] + '.jpg')
            # update database
            if remote_chapter > local_chapter:
                url = base_url + '/' + str(id)
                payload = {
                    'state': remote_state,
                    'curchapter': remote_chapter
                }
                r = requests.put(url, data=payload)
                print r.text


def comic_init():
    # get all comics from database
    id_list = ['200103359', '200103364', '200103379', '200103383', '200103388', '200103408', '200103424', '200103454',
               '200103457', '200103377', '200103380', '200103382', '200103386', '200103391', '200103393', '200103394',
               '200103396', '200103398', '200103401', '200103403', '200103405']

    # ftp init
    # myftp = MyFTP('202.102.41.224', 21, 'admin', 'admin123', '.')
    # myftp.login()

    # log in
    login_url = 'http://www.icartoons.cn/index.php?m=member&c=index&a=login'
    s = requests.Session()
    payload = {
        'username': '18118999630',
        'password': '1q2w3e4r',
        'dosubmit': '1'
    }
    r = s.post(login_url, data=payload)
    #
    for id in id_list:
        # requests
        request_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=show&catid=25&id=%s' % id
        r = s.get(request_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        content_soup = soup.find(class_='de_content')
        #print content_soup
        cover_soup = content_soup.find('img')
        cover = cover_soup['src']
        name_soup = content_soup.find('h1')
        name = name_soup.string

        author_soup = content_soup.find_all('a')
        author = author_soup[1].string

        brief_soup = content_soup.find(class_='introdu')
        brief = brief_soup.p.string

        state = re.search(u'状态：(&nbsp;)+(.*)<', r.text).group(2)
        categroy = re.search(u'题材：(&nbsp;)+(.*)<', r.text).group(2)

        hits = re.search(u'人气：(&nbsp;)+(.*)<', r.text).group(2)

        curchapter = 0
        for a_tag in soup.find_all('a'):
            if re.search(u'第\d+集', a_tag.get_text()):
                curchapter += 1
        print cover,name,author,brief.strip(),'1' if state=='u已完结' else '0',categroy,hits,curchapter/2

        url = 'http://127.0.0.1:5000/api/v1.0/comics'
        data = {
            'id':id,
            'comicname':name,
            'cover':cover,
            'author':author,
            'brief':brief,
            'state':'1' if state=='u已完结' else '0',
            'hits':hits,
            'category':categroy,
            'packageid':12,
            'curchapter':curchapter/2,
            'freechapter':0
        }
        r = requests.post(url, data=data)

def readings_job():
    base_url = 'http://127.0.0.1:5000/api/v1.0/readings'
    host = 'http://wap.tyread.com'
    url = 'http://wap.tyread.com/baoyueInfoListAction.action?is_ctwap=0&monthProductId=169124282&pageNo=2'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    }
    _cookies = {
        'sso': 'LXy41MoZCDAXdOjFg2UYFOKLe0',
        'user': '156AE3C7CACD1C57FD3195D231C155CFD876717B5CE40DBA03EDC5ACCD9B5F2792A9FBE04496D49414FE1F6C78B50EC31287A1A6E02A11BC9EB61D971482DCD573D04B83155AD4BC70D8AE740057F6496AAA4A0E0D32A57B753A4849573B2A267759EA3A641DCF387E90C56C833B82022D4643C2893D0330BE750A9D96A450309B2D2C6115315B8B08313DD43835D266FF472CDCF0AF85913D1D4951104A65A6494CBF43D13161644699242FDD819454DF9F2A2BD906DC3D90E06AE622939D73A6CA03FB60627AD131D975BF1DA71658F00B03CCA5FEAF5C',
        'JSESSIONID': 'C9E5BBC28106F2AEC0B67F4988C6BFFF'
    }
    s = requests.Session()
    r = s.get(url, headers=headers, cookies=_cookies)
    r.encoding = 'utf-8'
    print r.text
    soup = BeautifulSoup(r.text, 'html.parser')
    book_url_tags = soup.find_all(href=lambda href: href and re.compile("^/bookdetail/").search(href))

    def confir(str):
        for i in range(0, 32):
            str = str.replace(chr(i), '')
        return str

    for book_url in book_url_tags:
        url = host + book_url['href'].strip()
        print url
        r = requests.get(url, headers=headers, cookies=_cookies)
        # print r.text
        soup = BeautifulSoup(r.text, 'html.parser')
        # print soup
        cover_tag = soup.find('img', src=lambda src: src and re.compile("\.jpg$").search(src))
        cover_url = cover_tag['src']
        m = re.search(u"content=\"(\S+)?,手机在线阅读。作者：(\S+)? ,分类：(\S+)?,已更新：(\d+)章,进度：(\S+)?,点击量：(\d+)?。作品介绍：(\S+)\"", r.text)
        if m:
            name = m.group(1)
            author = m.group(2)
            category = m.group(3)
            curchapter = m.group(4)
            state = m.group(5)
            hits = m.group(6)
            brief = m.group(7)
        m = re.search(r'bookId=(\d+)&', r.text)
        bookid = m.group(1)
        print bookid, name, author, category,curchapter,state, hits, cover_url, brief
        # updata database
        url = 'http://127.0.0.1:5000/api/v1.0/readings'
        data = {
            'bookid': bookid,
            'name': name,
            'author': author,
            'packageid': 19,
            'state': '1' if state.encode("UTF-8") == '已完本' else '0',
            'hits': hits,
            'cover': cover_url,
            'brief': brief,
            'curchapter': curchapter,
            'freechapter': curchapter,
            'category':category
        }
        r = requests.post(url, data=data)
        print r.text

        # 获取书本内容
        # menu_url = 'http://wap.tyread.com/bookdetail/%s/gobookdescription.html?is_ctwap=0&pagesize=10000&orderBy=0' % bookid
        # r = requests.get(menu_url, headers=headers, cookies=_cookies)
        # soup = BeautifulSoup(r.text, 'html.parser')
        # menutag = soup.find_all(href=lambda href: href and re.compile("^/goChapterContent.action").search(href))
        # url = 'http://127.0.0.1:5000/api/v1.0/chapters'
        # i = 1
        # for tag in menutag:
        #     chapter_name = tag.string
        #     chapter_url = host + tag['href']
        #     r = requests.get(chapter_url, headers=headers, cookies=_cookies)
        #     m = re.search(r'<div style=\"overflow:hidden;\">(.*?)</div>', r.text, re.S)
        #     print chapter_name
        #     if m:
        #         chapter_content = '<p>    ' + m.group(1).strip()
        #         # print chapter_content
        #         data = {
        #             'chapterid': i-1,
        #             'chaptername': chapter_name,
        #             'content': chapter_content,
        #             'bookid': bookid
        #         }
        #         r = requests.post(url, data=data)
        #         print r.text
        #     i = i + 1


readings_job()
#comic_init()
