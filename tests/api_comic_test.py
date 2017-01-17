#-*-coding:utf-8-*-
import requests

base_url = 'http://127.0.0.1:5000/api/v1/comics'


def add_test():
    url = base_url
    payload = {
        'comicid':'200099420',
        'comicname':'混沌少女3',
        'packageid':'1',
        'brief':'《混沌少女3》是五个少年无意中开启了一所精神病院的保险柜，解开了混沌少女希希莉亚的封印。从而被混沌神少女选作混沌战士五小强，一幕幕超能力闹剧即将登场',
        'author':'图：张琨/文：张琨',
        'category':'神魔',
        'hits':10000,
        'state':'0',
        'cover':'www.baidu.com',
        'curchapter':0,
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