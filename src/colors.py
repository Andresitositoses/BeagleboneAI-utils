# Colors
WHITE = "\033[0m"
PURPLE = "\033[95m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"
ORANGE = "\033[93m"
BROWN = "\033[33m"


def get_painted_list(color_getter_function, list_to_paint, default_color=WHITE):
    '''
    Returns a list with the specified color
    '''
    painted_list = []
    for item in list_to_paint:
        painted_list.append(f"{color_getter_function(item)}{item}{default_color}")
    return painted_list