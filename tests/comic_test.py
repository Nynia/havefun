# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import re
import os
from app.utils.ftp import MyFTP
import config
def update_comics(id):
    login_url = 'http://www.icartoons.cn/index.php?m=member&c=index&a=login'
    # login
    s = requests.Session()
    payload = {
        'username': '18118999630',
        'password': '1q2w3e4r',
        'dosubmit': '1'
    }
    r = s.post(login_url, data=payload)
    print r.text
    # requests
    request_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=show&catid=25&id=%s' % id
    r = s.get(request_url)
    # check state
    match = re.search(u'状态：(&nbsp;)+(.*)<', r.text)
    if match:
        state = match.group(2)
        if state == u'已完结':
            print id, state
            #return
    myftp = MyFTP(config.FTP_ADDR, config.FTP_PORT, config.FTP_USER, config.FTP_PWD, '/')
    #myftp = MyFTP('61.160.185.51', 11145, 'jsgx', 'jsgx2017', '.')
    myftp.login()
    soup = BeautifulSoup(r.text, 'html.parser')
    for a_tag in soup.find_all('a'):
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
                    print img_tag['id'], img_tag['src']
                    if len(img_tag['src']) < 30:
                        continue
                    target_name = '_'.join((id, episode, img_tag['id'][3:])) + '.jpg'
                    target_dir = id + os.sep + episode
                    # download pics
                    # myftp.changewd('comic/20082903/123')
                    myftp.uploadFiles(img_tag['src'], 'comics/'+id+'/'+episode, img_tag['id'][3:]+'.jpg')
                    #with open(target_path, 'wb') as handle:
                    #    response = requests.get(img_tag['src'], stream=True)
                    #    for block in response.iter_content(1024):
                    #        if not block:
                    #            break
                    #        handle.write(block)
                    #upload_qiniu(target_path, target_name)
update_comics('200084970')