from . import api
from flask import request, jsonify
import time

CLIENT_ID = '8148610453'
APP_SECRET = 'DeAEsBOFlMuhPoCkJqGAniMqthO1q5dK'

@api.route('/tyopen/callback', methods=['POST'])
def getuserinfo():
    accessToken = request.form.get('accessToken')
    loginMode = request.form.get('loginMode')

    data = {
        'clientId': CLIENT_ID,
        'timestamp': str(int(round(time.time() * 1000))),
        'accessToken': accessToken,
        'version': 'v1.5',
        'clientIp': '127.0.0.1',
    }

    print data


