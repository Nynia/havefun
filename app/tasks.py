#-*-coding:utf-8-*-
from app import db
import requests
from flask import jsonify
#更新漫画到七牛云
def comic_job():
    #从数据库获取所有漫画信息
    url = 'http://127.0.0.1:5000/api/v1/comics'
    r = requests.get(url)
    json_result = r.json()
    if json_result['code'] == '0':
        data = json_result['data']
        for item in data:
            id = item['comicid']


comic_job()