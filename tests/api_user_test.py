import requests

base_url = 'http://127.0.0.1:5000/api/v1/users'

def test_1():
    url = base_url
    payload = {
        'limit':2,
        'offset':3
    }
    r = requests.get(url, params=payload)
    print r.url
    print r.text

def test_2():
    url = base_url
    data = {
        'phonenum':'18118999631',
        'password':'12345',
        'nickname':'sk'
    }
    r = requests.post(url, data=data)
    print r.text

def test_3():
    url = base_url + '/12'
    data = {
        'password':'1q2w3e4r'
    }
    r = requests.put(url, data=data)
    print r.text

def test_4():
    url = base_url + '/11'
    r = requests.delete(url)
    print r.text
#test_1()
#test_2()
test_3()
test_4()