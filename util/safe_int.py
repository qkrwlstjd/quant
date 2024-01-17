def safe_cast_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0