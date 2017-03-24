import hashlib
from datetime import datetime

def generate_name(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    postfix = filename[filename.rfind('.')+1:]
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