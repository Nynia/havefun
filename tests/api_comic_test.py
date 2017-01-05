import requests

base_url = 'http://127.0.0.1:5000/api/v1/comics'


def add_test():
    url = base_url
    payload = {
        'comicid':'1002',
        'comicname':'test2',
        'packageid':'1',
        'brief':'induction',
        'author':'sk',
        'category':'rexue',
        'hits':10000,
        'state':'1',
        'cover':'www.baidu.com',
        'curchapter':100,
        'freechapter':20
    }
    r = requests.post(url, data=payload)
    print r.text
def query_test():
    url = base_url + '/1001'
    r = requests.get(url)
    print r.text

def modify_test():
    url = base_url + '/1001'
    payload = {
        'brief':'brief',
        'hits':10001
    }
    r = requests.put(url, data=payload)
    print r.text

def delete_test():
    url = base_url + '/1001'
    r = requests.delete(url)
    print r.text
add_test()
query_test()
#modify_test()
#delete_test()