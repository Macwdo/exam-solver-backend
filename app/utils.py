import os
import tempfile
from contextlib import contextmanager
from time import perf_counter


def time_it(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Time taken to {func.__name__}: {end - start} seconds")
        return result

    return wrapper


@contextmanager
def create_temp_file(extension: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
        yield temp_file.name

    os.remove(temp_file.name)
