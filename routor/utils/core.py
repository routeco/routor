from routor.weights import WeightFunction


def import_weight_function(path: str) -> WeightFunction:
    """
    Imports a weight function from a string.
    """
    from importlib import import_module

    module_path, func_name = path.rsplit('.', 1)
    module = import_module(module_path)
    weight_func = getattr(module, func_name)

    return weight_func
