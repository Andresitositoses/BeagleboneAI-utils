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


def get_painted_list(color_getter_function, list_to_paint, selected_pins_map=None, default_color=WHITE, available_color=GREEN, unavailable_color=RED):
    '''
    Returns a list with the specified color
    '''
    painted_list = []
    if selected_pins_map is None: # There aren't highlighted pins --> Paint all the list with no distinction
        for item in list_to_paint:
            painted_list.append(f"{color_getter_function(item)}{item}{default_color}")
    else:
        for i, item in enumerate(list_to_paint):
            if not list_has_element(["gnd", "vout", "vin", "vdd", "ain", "pwr", "sys"], item.lower()):
                painted_list.append(f"{available_color if selected_pins_map[i] else unavailable_color}{item}{default_color}")
            else:
                painted_list.append(f"{color_getter_function(item)}{item}{default_color}")
    return painted_list

def list_has_element(list, elem):
    '''
    Returns True if the list passed as parameter has the element passed as parameter.
    '''
    for list_i in list:
        if list_i in elem:
            return True
    return False