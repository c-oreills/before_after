"""Package for before_after."""

__project__ = 'before_after'
__version__ = '0.1.3'

VERSION = __project__ + '-' + __version__

PYTHON_VERSION = 2, 7

import sys
if not sys.version_info >= PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))


from contextlib import contextmanager
from functools import wraps


def before(target, fn, **kwargs):
    return before_after(target, before_fn=fn, **kwargs)


def after(target, fn, **kwargs):
    return before_after(target, after_fn=fn, **kwargs)


@contextmanager
def before_after(
        target, before_fn=None, after_fn=None, once=True, **kwargs):
    def before_after_wrap(fn):
        called = []

        @wraps(fn)
        def inner(*a, **k):
            # If once is True, then don't call if this function has already
            # been called
            if once:
                if called:
                    return fn(*a, **k)
                else:
                    # Hack for lack of nonlocal keyword in Python 2: append to
                    # list to maked called truthy
                    called.append(True)

            if before_fn:
                before_fn(*a, **k)
            ret = fn(*a, **k)
            if after_fn:
                after_fn(*a, **k)
            return ret
        return inner

    from mock import patch

    patcher = patch(target, **kwargs)
    original, _ = patcher.get_original()
    with patcher as mock_fn:
        mock_fn.side_effect = before_after_wrap(original)
        yield
