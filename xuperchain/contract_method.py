from functools import wraps

def contract_method(f):
     # @wraps(f)
     def wrapper(*args, **kwds):
         return f(*args, **kwds)
     return wrapper