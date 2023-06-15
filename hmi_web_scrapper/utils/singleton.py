import threading

class Singleton(object):
    _instance = None
    curr_e_standard = None
    app_path = None
    lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance