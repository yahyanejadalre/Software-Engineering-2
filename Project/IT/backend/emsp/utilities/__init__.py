def jsonfield_default_value():  # This is a callable
    return [""]  # Any serializable Python obj, e.g. `["A", "B"]` or `{"price": 0}`


def rename_key(data: dict, source: str, target: str):
    if source not in data:
        return data
    data[target] = data.pop(source)
    return data


def noop(*args, **kwargs):
    pass
