# ----------------------------------------------------------------------------------------------------------------------
#  runtime.py
#
#  Contains a decorator function for getting the runtime of a function in seconds.
# ----------------------------------------------------------------------------------------------------------------------

from functools import wraps
from time import perf_counter

def runtime(function):
    """
    Decorator for getting the runtime of a function.
    :param function: The function to be decorated
    :return: The runtime of the function in seconds
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        function(*args, **kwargs)
        end_time = perf_counter()
        return function.__name__, end_time - start_time
    return wrapper
