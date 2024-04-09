def camel_to_snake(name):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


def convert_dict_to_snake(obj):
    if not isinstance(obj, dict):
        return obj
    return {camel_to_snake(k): convert_dict_to_snake(v) for k, v in obj.items()}