# -*- coding:utf-8 -*-

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64

class aescrypt():
    def __init__(self, key, iv='1234567812345678'):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        # 补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(text)
        # 把加密后的字符串转化为16进制字符串
        #return b2a_hex(ciphertext)
        # 返回加密字符串的base64值
        return base64.b64encode(ciphertext)

        # 解密后，去掉补足的空格用strip() 去掉

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(base64.b64decode(text))
        return self.unpad(plain_text.rstrip('\0'))


if __name__ == '__main__':
    pc = aescrypt('1234567812345678')  # 初始化密钥 和 iv

    e = pc.encrypt("123456")  # 加密
    d = pc.decrypt(e)  # 解密
    print "加密:", e
    print "解密:", d
    print "长度:", len(d)