import requests

base_url = 'http://127.0.0.1:5000/api/v1.0/favors'

def test_1():
    url = base_url + '/favor'
    data = {
        'uid':30,
        'cid':200103364,
        'type':'1'
    }
    r = requests.put(url, data=data)
    print r.text


def test_2():
    url = base_url + '/unfavor'
    data = {
        'uid':28,
        'cid':200103364,
        'type':'1'
    }
    r = requests.put(url, data=data)
    print r.text

def test_3():
    url = base_url + '/28'
    r = requests.get(url)
    print r.text
test_1()
#test_2()
#test_3()