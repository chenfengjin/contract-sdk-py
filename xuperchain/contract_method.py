from functools import wraps

def contract_method(f):
     # @wraps(f)
     def contract_method_wraper(*args, **kwds):
         return f(*args, **kwds)
     return contract_method_wraper