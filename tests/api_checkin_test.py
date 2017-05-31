#-*-coding:utf-8-*-
import requests

base_url = 'http://127.0.0.1:5000/auth'

def test_1():
    url = base_url + '/checkin'
    data = {
        'uid':28,
    }
    r = requests.get(url,params=data)
    print r.text

test_1()