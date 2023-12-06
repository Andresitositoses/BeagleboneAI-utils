import Adafruit_BBIO
import Adafruit_BBIO.GPIO as GPIO # Quizá pueda utilizar esto especificando el puerto del pin
import src.colors as colors

# Dimensions
PINOUT_ZONE_SIZE = 46
PINOUT_COLUMN_LENGTH = 23

MARGIN_SHOW = 15
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


    def show_pinout(self, filtered_pins=None, format=TWO_COLUMNS_FORMAT):

        if format == ONE_COLUMN_FORMAT:

            # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
            p9_left_spaces = 0
            for i in range(PINOUT_ZONE_SIZE):
                if filtered_pins:
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin)]
                else:
                    p9_left_i_list = self.p9_pins[i][0]
                aux_len = len(" ".join(p9_left_i_list))
                if aux_len > p9_left_spaces:
                    p9_left_spaces = aux_len
            
            print("\n\n")
            for i in range(PINOUT_ZONE_SIZE):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin)]
                    p8_left_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin)]
                else:
                    p9_left_i_list = self.p9_pins[i][0]
                    p8_left_i_list = self.p8_pins[i][0]

                aux_len = len(" ".join(p9_left_i_list))
                left_painted_list = colors.get_painted_list(get_color, p9_left_i_list)
                right_painted_list = colors.get_painted_list(get_color, p8_left_i_list)
                
                print(" " * (p9_left_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}"
                    + " " * (3 - len(str(i + 1)) + 1) + "|  " + " ".join(right_painted_list))

        else: # TWO_COLUMN_FORMAT 

            p9_left_spaces = 0
            p9_right_spaces = 0
            p8_left_spaces = 0
            for i in range(0, PINOUT_ZONE_SIZE, 2):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin)]
                    p9_right_i_list = [pin for pin in self.p9_pins[i+1][0] if list_has_element(filtered_pins, pin)]
                    p8_left_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin)]
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

            print("\n\n")
            for i in range(0, PINOUT_ZONE_SIZE, 2):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    #p9_left_i_list = [pin for pin in self.p9_pins[i][0] if pin in str(filtered_pins)] # if filtered_pins has pin
                    p9_left_i_list = [pin for pin in self.p9_pins[i][0] if list_has_element(filtered_pins, pin)]
                    p9_right_i_list = [pin for pin in self.p9_pins[i+1][0] if list_has_element(filtered_pins, pin)]
                    p8_left_i_list = [pin for pin in self.p8_pins[i][0] if list_has_element(filtered_pins, pin)]
                    p8_right_i_list = [pin for pin in self.p8_pins[i+1][0] if list_has_element(filtered_pins, pin)]
                else:
                    p9_left_i_list = self.p9_pins[i][0]
                    p9_right_i_list = self.p9_pins[i+1][0]
                    p8_left_i_list = self.p8_pins[i][0]
                    p8_right_i_list = self.p8_pins[i+1][0]

                p9_left_painted_list = colors.get_painted_list(get_color, p9_left_i_list)
                p9_right_painted_list = colors.get_painted_list(get_color, p9_right_i_list)
                p8_left_painted_list = colors.get_painted_list(get_color, p8_left_i_list)
                p8_right_painted_list = colors.get_painted_list(get_color, p8_right_i_list)

                
                print(" " * (p9_left_spaces - len(" ".join(p9_left_i_list))) + " " * MARGIN_SHOW + " ".join(p9_left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}{i+1} -- P9 -- {i+2}{colors.WHITE}"
                    + " " * (3 - len(str(i+2 + 1)) + 1) + "|  " + " ".join(p9_right_painted_list)
                    + " " * MARGIN_SHOW + " " * (p9_right_spaces - len(" ".join(p9_right_i_list))) + "."
                    + " " * (p8_left_spaces - len(" ".join(p8_left_i_list))) + " " * MARGIN_SHOW + " ".join(p8_left_painted_list) + "  |" + " " * (3 - len(str(i + 1)) + 1) + f"{colors.PURPLE}{i+1} -- P8 -- {i+2}{colors.WHITE}"
                    + " " * (3 - len(str(i+2 + 1)) + 1) + "|  " + " ".join(p8_right_painted_list))            
            

    def show_P8_pinout(self):
        '''
        Displays the ports disposed on the P8 zone in the physical position they are.
        '''
        for pin in self.p8_pins:
            print(pin)

    def show_P9_pinout(self):
        '''
        Displays the ports disposed on the P9 zone in the physical position they are.
        '''
        for pin in self.p9_pins:
            print(pin)

    def show_GPIO_ports(self):
        '''
        Displays the available GPIOs ports.
        The ones which are showed with green color indicates they are activated.
        '''
        df = open("/sys/class/grpio", "w+")
        

    def show_AIN_ports(self):
        '''
        Display the available Analogic ports.
        The ones which are showed with green color indicates they are activated.
        '''
        print("")
