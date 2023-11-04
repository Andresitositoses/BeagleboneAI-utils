import Adafruit_BBIO
import Adafruit_BBIO.GPIO as GPIO

PINOUT_ZONE_SIZE = 46
PINOUT_COLUMN_LENGTH = 23

def load_pinout_config(config_file):
    '''
    Parse the specified file to load the different modes of each pin of zones P8 and P9
    '''
    df = open(config_file, "r")

    p8_modes = []
    p9_modes = []

    # Config file lines
    for index, line in enumerate(df.readlines()):
        if (index < PINOUT_COLUMN_LENGTH):
            p8_entry = []
            for mode in line.split("|")[1].split(" "):
                p8_entry.append(mode)
            p8_entry[-1] = p8_entry[-1][:-1] # Remove last item's \n
            p8_modes.append(p8_entry[1:]) # Remove first space

        else:
            p9_entry = []
            for mode in line.split("|")[1].split(" "):
                p9_entry.append(mode)
            p9_entry[-1] = p9_entry[-1][:-1] # Remove last item's \n
            p9_entry.append(p9_entry[1:]) # Remove first space

    return p8_modes, p9_modes

class PinsManager():
    
    def __init__(self):
        
        # Load pins configuration file
        #self.file = open("/opt/source/dtb-4.14-ti/src/arm/am5729-beagleboneai-roboticscape.dts", "r")

        # Pin modes listed by help(Adafruit_BBIO)
        self.modes_availables = ["ADC", "Encoder", "GPIO", "PWM", "SPI", "UART", "sysfs"]

        self.p8_pins, self.p9_pins = load_pinout_config("files/pins_modes")

    def show_pinout(self):
        
        for i in range(PINOUT_ZONE_SIZE):
            if (len(str(i+1)) < 2):
                print(f"{self.p9_pins[i]}  |   P9_{i+1} --- P8_{i+1}   |  {self.p8_pins[i]}")
            else:
                print(f"{self.p9_pins[i]}  |  P9_{i+1} --- P8_{i+1}  |  {self.p8_pins[i]}")

    def show_P8_pinout(self):
        for pin in self.p8_pins:
            print(pin)

    def show_P9_pinout(self):
        for pin in self.p9_pins:
            print(pin)