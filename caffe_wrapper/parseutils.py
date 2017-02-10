import ast
import numpy as np

def get_param_value(param):
    if (param.startswith("np.array(")):
        arr = param[9:][:-1]
        value = np.array(ast.literal_eval(arr))
    else:
        value = ast.literal_eval(param)
    return value

