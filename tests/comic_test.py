# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import re
import os
import config

def upload_qiniu(img_url, target_name):
    from qiniu import Auth, put_file, etag, urlsafe_base64_encode
    import qiniu.config

    # 需要填写你的 Access Key 和 Secret Key
    access_key = config.QINIU_ACCESS_KEY
    secret_key = config.QINIU_SECRET_KEY

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'comic'

    # 上传到七牛后保存的文件名
    key = target_name;

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = img_url

    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


def upload_comics(id):
    login_url = 'http://www.icartoons.cn/index.php?m=member&c=index&a=login'
    # login
    s = requests.Session()
    payload = {
        'username': '18118999630',
        'password': '1q2w3e4r',
        'dosubmit': '1'
    }
    r = s.post(login_url, data=payload)

    # requests
    request_url = 'http://www.icartoons.cn/index.php?m=content&c=index&a=show&catid=25&id=%s' % id
    r = s.get(request_url)
    # check state
    match = re.search(u'状态：(&nbsp;)+(.*)<', r.text)
    if match:
        state = match.group(2)
        if state == u'已完结':
            print id, state
            return

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
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    # download pics
                    target_path = target_dir + os.sep + img_tag['id'][3:] + '.jpg'
                    with open(target_path, 'wb') as handle:
                        response = requests.get(img_tag['src'], stream=True)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            handle.write(block)
                    upload_qiniu(target_path, target_name)

upload_comics('200084970')
