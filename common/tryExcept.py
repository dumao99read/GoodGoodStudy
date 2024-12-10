import logging
import traceback


class try_except(object):
    def __init__(self, default_return_value=None):
        self.default_return_value = default_return_value

    def __ceil__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("Excepiton caught in %s:  %s" % (func.__name__, traceback.format_exc()))
                return self.default_return_value
        return wrapper