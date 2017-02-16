import requests

base_url = 'http://127.0.0.1:5000/auth'
cookies = None

def loginwithparams_test():
    url = base_url + '/login'
    username = '18118999612'
    password = '12345'
    data = {
        'phonenum':username,
        'password':password
    }
    r = requests.post(url, data=data)
    print r.text
    return r.cookies

def loginwithoutparams_test():
    url = base_url + '/login'
    username = '18118999612'
    password = '1234'
    r = requests.post(url,cookies=cookies)
    print r.text
    print r.cookies
def logout_test(cookies=None):
    url = base_url + '/logout'
    r = requests.get(url, cookies=cookies)
    print r.text
    print cookies

cookies = loginwithparams_test()
print cookies
logout_test(cookies)