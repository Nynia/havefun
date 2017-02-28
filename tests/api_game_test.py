#-*-coding:utf-8-*-
import requests

base_url = 'http://127.0.0.1:5000/api/v1.0/games'

def add_test():
    url = base_url
    data = {
        'packageid':2,
        'name':'testgame2',
        'img_small':'http://www.baidu.com',
        'type':'2',
        'url':'http://www.cn2.com',
        'category':'ccc',
        'star':2,
        'brief':'dddsdfsafa',
        'size':'3.1',
    }
    r = requests.post(url, data=data)
    print r.text

def get_test():
    url = base_url + '/1'
    r = requests.get(url)
    print r.text

def get_all_test():
    url = base_url + '?type=1'
    r = requests.get(url)
    print r.text

def update_test():
    url = base_url + '/1'
    data = {
        'name':'testgam2update3',
        'type':'1',
        'star':4
    }
    r = requests.put(url, data=data)
    print r.text

def delete_test():
    url = base_url + '/1'
    r = requests.delete(url)
    print r.text


if __name__ == "__main__":
    pass