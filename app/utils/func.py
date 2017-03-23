import hashlib
from datetime import datetime

def generate_name(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    postfix = filename[filename.rfind('.')+1:]
    m = hashlib.md5()
    m.update(filename + timestamp)
    return m.hexdigest()[::2] + '.' + postfix

def generate_identifying_code():
    import random
    temp = ''
    for i in range(6):
        num = random.randrange(0, 6)
        if num == 3 or num == 1:
            rad2 = random.randrange(0, 10)

            temp = temp + str(rad2)

        else:
            rad1 = random.randrange(65, 91)
            c1 = chr(rad1)
            temp = temp + c1
    return temp