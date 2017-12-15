import hashlib
from datetime import datetime
from Crypto.Cipher import AES
import base64
import json


def generate_name(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    postfix = filename[filename.rfind('.') + 1:]
    m = hashlib.md5()
    m.update(filename + timestamp)
    return m.hexdigest()[::2] + '.' + postfix


def generate_identifying_code(len=4):
    import random
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, len)
    verification_code = ''.join(myslice)
    return verification_code

def generate_channel_token(name):
    timestamp = datetime.now().strftime('%m%d%H%M%S')
    m = hashlib.md5()
    m.update(name+timestamp)
    return m.hexdigest()[::2]

def AES_encrypt(text):
    key = 'Hlkj@~_^&&123_78'
    iv = '0201080306050704'
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrppted = ''
    for ch in encrypt_text:
        encrppted += chr(((ord(ch) >> 4) & 0xF) + ord('a'))
        encrppted += chr((ord(ch) & 0xF) + ord('a'))
    return encrppted
