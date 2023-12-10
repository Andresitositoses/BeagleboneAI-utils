import src.colors as colors
import os

# Dimensions
PINOUT_ZONE_SIZE = 46
PINOUT_COLUMN_LENGTH = 23

MARGIN_SHOW = 10
ONE_COLUMN_FORMAT = 0
TWO_COLUMNS_FORMAT = 1

def load_pinout_config(config_file):
    '''
    Parse the specified file to load the different modes of each pin of zones P8 and P9
    '''
    df = open(config_file, "r")

    p8_pins = [] # List of tuples ([modes], [buses])
    p9_pins = [] # List of tuples ([modes], [buses])

    # Config file lines
    for index, line in enumerate(df.readlines()):
        if (index < PINOUT_ZONE_SIZE):
            p8_entry_modes = []
            for mode in line.split("|")[1].split("@")[0].split(" "):
                p8_entry_modes.append(mode)
            p8_entry_buses = []
            try:
                for bus in line.split("|")[1].split("@")[1].split(" "):
                    p8_entry_buses.append(bus)
            except:
                p8_entry_modes[-1] = p8_entry_modes[-1][:-1] # Remove last item's \n (There are not buses, so the '\n' character is on the last mode)
            else:
                p8_entry_buses[-1] = p8_entry_buses[-1][:-1] # Remove last item's \n (The '\n' is on the last bus)
            p8_pins.append((p8_entry_modes[1:], p8_entry_buses)) # Remove first space

        else:
            p9_entry_modes = []
            for mode in line.split("|")[1].split("@")[0].split(" "):
                p9_entry_modes.append(mode)
            p9_entry_buses = []
            try:
                for bus in line.split("|")[1].split("@")[1].split(" "):
                    p9_entry_buses.append(bus)
            except:
                p9_entry_modes[-1] = p9_entry_modes[-1][:-1] # Remove last item's \n (There are not buses, so the '\n' character is on the last mode)
            else:
                p9_entry_buses[-1] = p9_entry_buses[-1][:-1] # Remove last item's \n (The '\n' is on the last bus)
            p9_pins.append((p9_entry_modes[1:], p9_entry_buses)) # Remove first space

    return p8_pins, p9_pins

def get_gpio_states():
    '''
    Returns a list of tuples with the GPIOs states
    '''
    gpio_states = []

def get_color(mode):
    '''
    Returns the color of the mode passed as parameter.
    '''
    if "GPIO" in mode:
        return colors.GREEN
    elif "AIN" in mode:
        return colors.CYAN
    elif "PWM" in mode:
        return colors.YELLOW
    elif "UART" in mode:
        return colors.PURPLE
    elif "SPI" in mode:
        return colors.RED
    elif "I2C" in mode:
        return colors.BLUE
    elif "3V3" in mode or "5V" in mode or "VDD" in mode:
        return colors.BROWN
    elif "GND" in mode:
        return colors.ORANGE
    else:
        return colors.WHITE

def list_has_element(list, elem):
    '''
    Returns True if the list passed as parameter has the element passed as parameter.
    '''
    for list_i in list:
        if list_i in elem:
            return True
    return False

class PinsManager():
    
    def __init__(self):
        
        # Load pins configuration file
        #self.file = open("/opt/source/dtb-4.14-ti/src/arm/am5729-beagleboneai-roboticscape.dts", "r")

        self.p8_pins, self.p9_pins = load_pinout_config("files/pins_modes")

        # Update pins status
        self.refresh_gpio_list()

        # Pins which are not availables
        self.enabled_buses = []
        self.enabled_buses += self.gpio_list_enabled
        #self.enabled_buses.append(self.ain_list_enabled)
        #self.enabled_buses.append(self.pwm_list_enabled)
        #self.enabled_buses.append(self.i2c_list_enabled)
        #self.enabled_buses.append(self.spi_list_enabled)
        #self.enabled_buses.append(self.uart_list_enabled)


    def refresh_gpio_list(self):

        # List directories from the /sys/class/gpio folder
        self.gpio_list_enabled = os.listdir("/sys/class/gpio")
        # Filter the list to only the GPIOs
        self.gpio_list_enabled = [gpio[4:] for gpio in self.gpio_list_enabled if gpio.startswith("gpio") and "chip" not in gpio]

    def show_pinout(self, format=TWO_COLUMNS_FORMAT, filtered_pins=None, show_enabled=False, get_color_function=get_color):

        if format == ONE_COLUMN_FORMAT:

            # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
            p9_left_spaces = 0
            for i in range(PINOUT_ZONE_SIZE):
                if filtered_pins:
                    p9_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                else:
                    p9_i_list = self.p9_pins[i][0]
                aux_len = len(" ".join(p9_i_list))
                if aux_len > p9_left_spaces:
                    p9_left_spaces = aux_len
            
            print("\n")
            for i in range(PINOUT_ZONE_SIZE):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                    p8_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                else:
                    p9_i_list = self.p9_pins[i][0]
                    p8_i_list = self.p8_pins[i][0]

                # Get asociated status for each pin
                p9_entry_status = None
                p8_entry_status = None

                if show_enabled and len(self.enabled_buses) > 0:
                    p9_entry_status = [(pin not in self.enabled_buses) for pin in self.p9_pins[i][1]]
                    p8_entry_status = [(pin not in self.enabled_buses) for pin in self.p8_pins[i][1]]

                aux_len = len(" ".join(p9_i_list))
                left_painted_list = colors.get_painted_list(get_color_function, p9_i_list, selected_pins_map=p9_entry_status)
                right_painted_list = colors.get_painted_list(get_color_function, p8_i_list, selected_pins_map=p8_entry_status)
                
                print(" " * (p9_left_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}"
                    + " " * (3 - len(str(i + 1)) + 1) + "|  " + " ".join(right_painted_list))

        else: # TWO_COLUMN_FORMAT 

            # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
            p9_left_spaces = 0
            p9_right_spaces = 0
            p8_left_spaces = 0
            for i in range(0, PINOUT_ZONE_SIZE, 2):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                    p9_right_i_list = [pin for pin in self.p9_pins[i+1][0] if list_has_element(filtered_pins, pin.lower())]
                    p8_left_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                else:
                    p9_left_i_list = self.p9_pins[i][0]
                    p9_right_i_list = self.p9_pins[i+1][0]
                    p8_left_i_list = self.p8_pins[i][0]

                aux_len = len(" ".join(p9_left_i_list))
                if aux_len > p9_left_spaces:
                    p9_left_spaces = aux_len

                aux_len = len(" ".join(p9_right_i_list))
                if aux_len > p9_right_spaces:
                    p9_right_spaces = aux_len

                aux_len = len(" ".join(p8_left_i_list))
                if aux_len > p8_left_spaces:
                    p8_left_spaces = aux_len

            print("\n")
            for i in range(0, PINOUT_ZONE_SIZE, 2):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                    p9_right_i_list = [pin for pin in self.p9_pins[i+1][0] if list_has_element(filtered_pins, pin.lower())]
                    p8_left_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin.lower())]
                    p8_right_i_list = [pin for pin in self.p8_pins[i+1][0] if list_has_element(filtered_pins, pin.lower())]
                else:
                    p9_left_i_list = self.p9_pins[i][0]
                    p9_right_i_list = self.p9_pins[i+1][0]
                    p8_left_i_list = self.p8_pins[i][0]
                    p8_right_i_list = self.p8_pins[i+1][0]

                # Get asociated status for each pin
                p9_left_status = None
                p9_right_status = None
                p8_left_status = None
                p8_right_status = None

                if show_enabled and len(self.enabled_buses) > 0:
                    p9_left_status = [(pin not in self.enabled_buses) for pin in self.p9_pins[i][1]]
                    p9_right_status = [(pin not in self.enabled_buses) for pin in self.p9_pins[i+1][1]]
                    p8_left_status = [(pin not in self.enabled_buses) for pin in self.p8_pins[i][1]]
                    p8_right_status = [(pin not in self.enabled_buses) for pin in self.p8_pins[i+1][1]]

                p9_left_painted_list = colors.get_painted_list(get_color_function, p9_left_i_list, selected_pins_map=p9_left_status)
                p9_right_painted_list = colors.get_painted_list(get_color_function, p9_right_i_list, selected_pins_map=p9_right_status)
                p8_left_painted_list = colors.get_painted_list(get_color_function, p8_left_i_list, selected_pins_map=p8_left_status)
                p8_right_painted_list = colors.get_painted_list(get_color_function, p8_right_i_list, selected_pins_map=p8_right_status)

                
                print(" " * (p9_left_spaces - len(" ".join(p9_left_i_list))) + " " * MARGIN_SHOW + " ".join(p9_left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}{i+1} -- P9 -- {i+2}{colors.WHITE}"
                    + " " * (3 - len(str(i+2 + 1)) + 1) + "|  " + " ".join(p9_right_painted_list)
                    + " " * MARGIN_SHOW + " " * (p9_right_spaces - len(" ".join(p9_right_i_list))) + "."
                    + " " * (p8_left_spaces - len(" ".join(p8_left_i_list))) + " " * MARGIN_SHOW + " ".join(p8_left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}{i+1} -- P8 -- {i+2}{colors.WHITE}"
                    + " " * (3 - len(str(i+2 + 1)) + 1) + "|  " + " ".join(p8_right_painted_list))

            print("") # New line

    def show_GPIO_ports(self):
        '''
        Displays the available GPIOs ports.
        The ones which are showed with green color indicates they are activated.
        The ones which are showed with red color indicates they are deactivated.
        '''
        
        # Update pins status
        self.refresh_gpio_list() # ¿Debería utilizar una función decoradora para que siempre se actualicen?

        self.show_pinout(filtered_pins=["gpio"], show_enabled=True)

        print("")
        

    def show_AIN_ports(self):
        '''
        Display the available Analogic ports.
        The ones which are showed with green color indicates they are activated.
        '''

        # Update pins status
        self.refresh_gpio_list()

        print("")