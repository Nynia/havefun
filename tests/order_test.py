import requests
import datetime
import hashlib
import json
def fun1():
    url = 'http://61.160.185.51:9250/ismp/serviceOrder'
    chargeid = '1971'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    secret = '13e69a3164d5fe59c683'
    token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
    spid = '35101296'
    phonenum = '18118999630'
    ordertype = '1'
    data = {
        'action': 'subscribe',
        'spId': spid,
        'chargeId': chargeid,
        'phoneNum': phonenum,
        'orderType': ordertype,
        'timestamp': timestamp,
        'accessToken': token
    }
    r = requests.post(url, data=data).text
    json_result = json.loads(r)
    print json_result

def func2():
    url = 'http://127.0.0.1:5000/api/v1.0/orders?action=unsubscribe'
    data = {
        'spid':'35101296',
        'chargeid':'1971',
        'secret':'13e69a3164d5fe59c683',
        'phonenum':'18118999630',
        'productid':'135000000000000229481'
    }
    r = requests.post(url, data=data)
    print r.text

def func3():
    url = 'http://127.0.0.1:5000/api/v1.0/orders/records/18118999630'
    r = requests.get(url)
    print r.text
func3()