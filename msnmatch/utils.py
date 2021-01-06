from msnmatch import settings
from hashlib import md5
from django.http import JsonResponse

def _error_response(message = ""):
    return JsonResponse({'message': message,'success': False})

def _success_response(data = None):
    ret_dict = {'success': True, 'message':"success"}
    if data:
        for k,v in data.items():
            ret_dict[k] = v
    return JsonResponse(ret_dict)

def _post_not_allowed():
    return _error_response("POST request not allowed")

def _get_not_allowed():
    return _error_response("GET request not allowed")

def js_boolean(val):
    if val == u"true":
        return True
    elif val == u"false":
        return False
    else:
        return -1

def custom_md5(pwd, salt):
    obj = md5()
    obj.update((pwd + salt).encode('utf-8'))
    return obj.hexdigest()

def cmp_int(a,b):
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

def cmp_semester(a,b):
    if a == b:
        return 0
    elif a == "":
        return -1
    elif b == "":
        return 1
    elif a[:4] != b[:4]:
        return cmp_int( int(a[:4]), int(b[:4]) )
    elif a[:4] == b[:4]:
        if a[4:] == "Fall":
            return 1
        elif b[4:] == "Fall":
            return -1
    return 0