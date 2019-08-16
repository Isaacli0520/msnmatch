from msnmatch import settings
from hashlib import md5

def custom_md5(pwd, salt):
    obj = md5()
    obj.update((pwd + salt).encode('utf-8'))
    return obj.hexdigest()