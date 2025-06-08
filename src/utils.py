from collections.abc import Iterable


def is_regular_iterable(obj):
    if isinstance(obj, str) or isinstance(obj, dict):
        return False

    return isinstance(obj, Iterable)
