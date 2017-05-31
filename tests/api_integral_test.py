#-*-coding:utf-8-*-
import requests

base_url = 'http://127.0.0.1:5000/api/v1.0/integral'

def test_add_new_strategy(value,desc):
    url = base_url + '/strategy'
    payload = {
        'value':value,
        'description':desc
    }
    r = requests.post(url,data=payload)
    print r.text

#test_add_new_strategy(20,'更换头像')
#test_add_new_strategy(20,'首次修改昵称')
#test_add_new_strategy(20,'玩H5游戏')
#test_add_new_strategy(20,'看动漫')
#test_add_new_strategy(20,'玩H5游戏')
#test_add_new_strategy(20,'收藏')
#test_add_new_strategy(200,'订购付费包')
#test_add_new_strategy(400,'首次订购付费包')
#test_add_new_strategy(100,'成功邀请好友')

#test_add_new_strategy(5,'连续签到1天')
#test_add_new_strategy(8,'连续签到2天')
#test_add_new_strategy(10,'连续签到3天')
#test_add_new_strategy(12,'连续签到4天')
#test_add_new_strategy(15,'连续签到5天')
#test_add_new_strategy(18,'连续签到6天')
#test_add_new_strategy(20,'连续签到7天及以上')


test_add_new_strategy(20,'连续登录1天')
test_add_new_strategy(23,'连续登录2天')
test_add_new_strategy(25,'连续登录3天')
test_add_new_strategy(27,'连续登录4天')
test_add_new_strategy(30,'连续登录5天')
test_add_new_strategy(22,'连续登录6天')
test_add_new_strategy(35,'连续登录7天')

#test_add_new_strategy(400,'注册帐号')

