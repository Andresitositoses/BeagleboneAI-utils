import Adafruit_BBIO
import Adafruit_BBIO.GPIO as GPIO

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

# Dimensions
PINOUT_ZONE_SIZE = 46
PINOUT_COLUMN_LENGTH = 23

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

class PinsManager():
    
    def __init__(self):
        
        # Load pins configuration file
        #self.file = open("/opt/source/dtb-4.14-ti/src/arm/am5729-beagleboneai-roboticscape.dts", "r")

        # Pin modes listed by help(Adafruit_BBIO)
        self.modes_availables = ["ADC", "Encoder", "GPIO", "PWM", "SPI", "UART", "sysfs"]

        self.p8_pins, self.p9_pins = load_pinout_config("files/pins_modes")

        # Shows the user the different functions are availables
        self.help()

    def help(self):
        print(f"{BLUE}##################################")
        print(f"##      Available commands      ##")
        print(f"##################################\n")
        print(" - PinsManager.help()            ")
        print(" - PinsManager.show_pinout()     ")
        print(" - PinsManager.show_P8_pinout()  ")
        print(" - PinsManager.show_P9_pinout()  ")
        print(" - PinsManager.show_GPIO_ports() ")
        print(" - PinsManager.show_AIN_ports()  ")
        print(f"{WHITE}\n")


    def show_pinout(self):

        # Useful to calculate the number of spaces to insert to each row in order to ajustate the showed info
        max_spaces = 0
        for i in range(PINOUT_ZONE_SIZE):
            aux_len = len(str(self.p9_pins[i][0]))
            if aux_len > max_spaces:
                max_spaces = aux_len
        
        for i in range(PINOUT_ZONE_SIZE):
            aux_len = len(str(self.p9_pins[i][0]))
            left_color = self.get_color(self.p9_pins[i][0])
            right_color = self.get_color(self.p8_pins[i][0])
            if (len(str(i+1)) < 2):
                print(" " * (max_spaces - aux_len) + f"{left_color}{self.p9_pins[i][0]}{WHITE}  |   {PURPLE}P9_{i+1} --- P8_{i+1}{WHITE}   |  {right_color}{self.p8_pins[i][0]}{WHITE}")
            else:
                print(" " * (max_spaces - aux_len) + f"{left_color}{self.p9_pins[i][0]}{WHITE}  |  {PURPLE}P9_{i+1} --- P8_{i+1}{WHITE}  |  {right_color}{self.p8_pins[i][0]}{WHITE}")

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
        print("")

    def show_AIN_ports(self):
        '''
        Display the available Analogic ports.
        The ones which are showed with green color indicates they are activated.
        '''
        print("")

    def get_color(self, modes):
        '''
        Returns the color of the mode passed as parameter.
        '''
        if "GPIO" in modes[0]:
            return GREEN
        elif "AIN" in modes[0]:
            return CYAN
        elif "PWM" in modes[0]:
            return YELLOW
        elif "UART" in modes[0]:
            return PURPLE
        elif "SPI" in modes[0]:
            return RED
        elif "I2C" in modes[0]:
            return BLUE
        elif "VOUT" in modes[0]:
            return ORANGE
        elif "GND" in modes[0]:
            return BROWN
        else:
            return WHITE