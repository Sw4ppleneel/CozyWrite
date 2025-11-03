import hashlib

def hash_data(data_string, algorithm='sha256'):
    hasher = getattr(hashlib, algorithm)()
    hasher.update(data_string.encode('utf-8'))
    return hasher.hexdigest()

def verify(user_password , db_password):
    if hash_data(user_password) == db_password :
        return 1
    else :
        return 0