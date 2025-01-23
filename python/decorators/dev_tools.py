from contextlib import contextmanager
import time


@contextmanager
def isolate_print(bar_length=40):
    print('-' * bar_length)
    yield
    print('-' * bar_length)


@contextmanager
def timed_test(description):
    start = time.time()
    yield
    dif_time = time.time() - start

    print('Timed Test ({}): {} seconds'.format(description, dif_time))