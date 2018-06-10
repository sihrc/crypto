from functools import wraps
from concurrent.futures import ThreadPoolExecutor

class ThreadPoolMixin(object):
    def __init__(self, num_workers):
        self._executor = ThreadPoolExecutor(num_workers)
    
    def execute_async(self, f, *args, **kwargs):
        if kwargs.pop("_sync", False):
            return f(*args, **kwargs)
        return self._executor.submit(f, *args, **kwargs)

    def wrap_async(self, func):
        @wraps(func)
        def thread_wrapper(*args, **kwargs):
            return self.execute_async(func, *args, **kwargs)
        return thread_wrapper
