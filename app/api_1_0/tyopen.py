from . import api
from flask import request, jsonify,session
import time

CLIENT_ID = '8148610453'
APP_SECRET = 'DeAEsBOFlMuhPoCkJqGAniMqthO1q5dK'

@api.route('/tyopen/callback', methods=['POST'])
def getuserinfo():
    accessToken = request.form.get('tyAccountToken')
    loginMode = request.form.get('tyloginMode')

    print accessToken, loginMode
    data = {
        'clientId': CLIENT_ID,
        'timestamp': str(int(round(time.time() * 1000))),
        'accessToken': accessToken,
        'version': 'v1.5',
        'clientIp': '127.0.0.1',
    }

    print data

    return jsonify({
        'code': '0',
        'message': 'success',
        'data':accessToken
    })