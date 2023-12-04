import Adafruit_BBIO
import Adafruit_BBIO.GPIO as GPIO
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

class PinsManager():
    
    def __init__(self):
        
        # Load pins configuration file
        #self.file = open("/opt/source/dtb-4.14-ti/src/arm/am5729-beagleboneai-roboticscape.dts", "r")

        self.p8_pins, self.p9_pins = load_pinout_config("files/pins_modes")


    def show_pinout(self, filtered_pins=None, format=TWO_COLUMNS_FORMAT):

        if format == ONE_COLUMN_FORMAT:
            # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
            max_spaces = 0
            for i in range(PINOUT_ZONE_SIZE):
                if filtered_pins:
                    p9_i_list = [pin for pin in filtered_pins if pin in str(self.p9_pins[i][0])]
                else:
                    p9_i_list = self.p9_pins[i][0]
                aux_len = len(" ".join(p9_i_list))
                if aux_len > max_spaces:
                    max_spaces = aux_len
            
            for i in range(PINOUT_ZONE_SIZE):

                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_i_list = [pin for pin in filtered_pins if pin in str(self.p9_pins[i][0])]
                    p8_i_list = [pin for pin in filtered_pins if pin in str(self.p8_pins[i][0])]
                else:
                    p9_i_list = self.p9_pins[i][0]
                    p8_i_list = self.p8_pins[i][0]

                aux_len = len(" ".join(p9_i_list))
                left_painted_list = colors.get_painted_list(get_color, p9_i_list)
                right_painted_list = colors.get_painted_list(get_color, p8_i_list)
                
                if (len(str(i+1)) < 2):
                    print(" " * (max_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + f"  |   {colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}   |  " + " ".join(right_painted_list))
                else:
                    print(" " * (max_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + f"  |  {colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}  |  " + " ".join(right_painted_list))
        
        else: # TWO_COLUMN_FORMAT 
            # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
            max_spaces = 0
            for i in range(PINOUT_ZONE_SIZE):
                if filtered_pins:
                    p9_i_list = [pin for pin in filtered_pins if pin in str(self.p9_pins[i][0])]
                else:
                    p9_i_list = self.p9_pins[i][0]
                aux_len = len(" ".join(p9_i_list))
                if aux_len > max_spaces:
                    max_spaces = aux_len

            for i in range(PINOUT_ZONE_SIZE):
                # Filter to pins in filtered_pins
                if filtered_pins is not None:
                    p9_i_list = [pin for pin in filtered_pins if pin in str(self.p9_pins[i][0])]
                    p8_i_list = [pin for pin in filtered_pins if pin in str(self.p8_pins[i][0])]
                else:
                    p9_i_list = self.p9_pins[i][0]
                    p8_i_list = self.p8_pins[i][0]

                aux_len = len(" ".join(p9_i_list))
                left_painted_list = colors.get_painted_list(get_color, p9_i_list)
                right_painted_list = colors.get_painted_list(get_color, p8_i_list)
                
                if (len(str(i+1)) < 2):
                    print(" " * (max_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + f"  |   {colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}   |  " + " ".join(right_painted_list))
                else:
                    print(" " * (max_spaces - aux_len) + " " * MARGIN_SHOW + " ".join(left_painted_list) + f"  |  {colors.PURPLE}P9_{i+1} --- P8_{i+1}{colors.WHITE}  |  " + " ".join(right_painted_list))

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
