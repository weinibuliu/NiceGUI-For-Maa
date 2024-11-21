import os
import threading

# Codes From https://pypi.org/project/pyngleton/


def singleton(cls):
    """
    Decorator for declaring the class as a thread-safe & process-safe singleton.
    """
    instances = {}
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        key = (os.getpid(), cls.__name__)
        if key not in instances:
            with lock:
                if key not in instances:
                    instances[key] = cls(*args, **kwargs)
        return instances[key]

    return wrapper
