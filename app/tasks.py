#-*-coding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup
from app.utils.ftp import MyFTP

def comic_job():
    #get all comics from database
    base_url = 'http://127.0.0.1:5000/api/v1/comics'
    r = requests.get(base_url)
    json_result = r.json()

    #ftp init
    myftp = MyFTP('202.102.41.224', 21, 'admin', 'admin123', '.')
    myftp.login()

    #log in
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
            id = item['comicid']
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
                #parse
                soup = BeautifulSoup(r.text, 'html.parser')
                for a_tag in soup.find_all('a'):
                    content = a_tag.get_text()
                    if re.search(u'第\d+集', content):
                        episode = re.search(u'第(\d+)集', content).group(1)
                        if int(episode) > remote_chapter:
                            remote_chapter = int(episode)
                        #update episode
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
                                    myftp.uploadFiles(img_tag['src'], 'comic/' + id + '/' + episode,
                                                      img_tag['id'][3:] + '.jpg')
            #update database
            if remote_chapter > local_chapter:
                url = base_url + '/' +id
                payload = {
                    'state':remote_state,
                    'curchapter':remote_chapter
                }
                r = requests.put(url, data=payload)
                print r.text

comic_job()