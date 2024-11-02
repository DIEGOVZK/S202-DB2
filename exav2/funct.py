from functools import wraps


def TryCatchAbstract(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper


class TryCatchAll(type):
    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if callable(value):
                dct[attr] = TryCatchAbstract(value)
        return super().__new__(cls, name, bases, dct)


def Listify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            if isinstance(result, list):
                return [list(item) if isinstance(item, (list, tuple)) else item for item in result]
            return list(result)
        return result
    return wrapper
