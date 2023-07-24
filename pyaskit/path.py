import sys
from contextlib import contextmanager


@contextmanager
def add_to_sys_path(new_path):
    """Context manager to temporarily add a directory to sys.path."""
    try:
        if new_path not in sys.path:
            sys.path.insert(0, new_path)
            added = True
        else:
            added = False
        yield
    finally:
        # Only remove the path if it was added by this context manager
        if added:
            sys.path.remove(new_path)
