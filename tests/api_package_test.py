#-*-coding:utf-8-*-
import requests

base_url = 'http://127.0.0.1:5000/api/v1.0/packages'
def test_1():
    url =  base_url + '/12'
    r = requests.get(url)
    print r.text
def test_2():
    payload = {
        'productid':'135000000000000229481',
        'productname':'乐游狂人包',
        'type':'2',
        'price': 10,
    }
    r = requests.post(base_url, data=payload)
    print r.text
def test_3():
    url = base_url
    print url
    r = requests.get(url)
    print r.text

def test_4():
    url = base_url +'/1'
    r = requests.delete(url)
    print r.text

def test_5():
    url = base_url + '/2'
    payload = {
        'packagename': 'test22222',
        'type': '1',
    }
    r = requests.put(url, data=payload)
    print r.text
#test_1()
test_2()
#test_5()
#test_5()