import requests

base_url = 'http://127.0.0.1:5000/api/v1/packages'
def test_1():
    url =  base_url + '/12'
    r = requests.get(url)
    print r.text
def test_2():
    payload = {
        'packageid':'3',
        'packagename':'test3',
        'type':'1',
        'price': 1,
        'description':'this is a test'
    }
    r = requests.post(base_url, data=payload)
    print r.text
def test_3():
    url = base_url + '?type=0'
    print url
    r = requests.get(url)
    print r.text

def test_4():
    url = base_url +'/6'
    r = requests.delete(url)
    print r.text

def test_5():
    url = base_url + '/2222'
    payload = {
        'packagename': 'test22222',
        'type': '1',
    }
    r = requests.put(url, data=payload)
    print r.text
test_1()
test_2()
#test_4()
#test_5()