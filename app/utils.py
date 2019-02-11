"""Various utils function."""


def safe_lower(val):
    if isinstance(val, str):
        return val.lower()
    return val
