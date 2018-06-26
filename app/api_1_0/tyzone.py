# -*- coding: UTF-8 -*-
from . import api
from flask import request, jsonify
from urllib import quote
import hashlib


@api.route('/tyzone/callback', methods=['POST', 'GET'])
def func():
    apsecret = '2027e1d246f3aa52f1c6ea786cc4ef4e'
    params = []
    sig2 = ''
    print request.form.to_dict()
    for key, value in request.form.to_dict().items():
        if key != 'sig':
            params.append((key, value))
        else:
            sig2 = value
    sorted_params = sorted(params)
    print sorted_params
    key_str = ''
    for params in sorted_params:
        if params[1] != '':
            key_str += params[0]
            key_str += params[1]
    print key_str
    key_quoted = quote(key_str)
    print key_quoted
    print sig2, hashlib.sha1(key_quoted + apsecret).hexdigest()
    if sig2 == hashlib.sha1(key_quoted + apsecret).hexdigest():
        return jsonify({
            'resultCode': '0000',
            'resultDesc': 'accepted'
        })
    else:
        return jsonify({
            'resultCode': '0001',
            'resultDesc': 'accept error'
        })
