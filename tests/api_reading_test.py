import requests

base_url = 'http://127.0.0.1:5000/api/v1.0/readings'

def test_1():
    data = {
        'bookid':'11111',
        'packageid':'2222222222',
        'name':'test',
        'author':'sk',
        'state':'1',
        'hits':50,
        'brief':'sfsfsf',
        'cover':'http://www.baidu.com',
        'curchapter':11,
        'freechapter':4
    }
    r = requests.post(base_url,data=data)
    print r.text

test_1()