from src.pinsManager import PinsManager
import src.pinsManager as pinsManager
import src.colors as colors

pm = PinsManager()

def help():
    
    # Clean the screen
    print("\033c\n\n\n", end="")

    print(" " * pinsManager.MARGIN_SHOW + f"{colors.BLUE}##################################")
    print(" " * pinsManager.MARGIN_SHOW + "##      Available commands      ##")
    print(" " * pinsManager.MARGIN_SHOW + "##################################\n")
    print(" " * pinsManager.MARGIN_SHOW + " - show all [--one-column]")
    print(" " * pinsManager.MARGIN_SHOW + " - show [type1] [type2] [typeN] [--one-column]")
    print(" " * pinsManager.MARGIN_SHOW + " - config <pin-mode>")
    print(" " * pinsManager.MARGIN_SHOW + " - help")
    print(" " * pinsManager.MARGIN_SHOW + " - clear")
    print(" " * pinsManager.MARGIN_SHOW + " - exit\n")
    print(f"{colors.WHITE}")

# Show the help
help()

while True:
    try:
        command = input(f"{colors.GREEN}PinsManager> {colors.WHITE}")

        command = command.split(" ")
        
        num_words = len(command)

        if (num_words != 0):

            parameters = None
            if num_words > 1:
                parameters = command[1:]
            command = command[0]

            if parameters is None: # Has no parameters
                if command == "exit":
                    break
                elif command == "help":
                    help()
                elif command == "clear" or command == "cls":
                    print("\033c\n\n\n", end="")
                else:
                    print(f"{colors.RED}Command not found{colors.WHITE}")

            else: # Has parameters
                if command == "show":

                    if parameters[0] == "all":
                        spec_format = pinsManager.ONE_COLUMN_FORMAT if parameters[-1] == "--one-column" else pinsManager.TWO_COLUMNS_FORMAT
                        pm.show_pinout(format=spec_format)
                    else:
                        spec_format = pinsManager.ONE_COLUMN_FORMAT if parameters[-1] == "--one-column" else pinsManager.TWO_COLUMNS_FORMAT
                        parameters = parameters[:-1] if parameters[-1] == "--one-column" else parameters
                        pm.show_pinout(format=spec_format, filtered_pins=parameters, show_enabled=True)
                    

                elif command == "config":
                    if (len(parameters) == 1):
                        if parameters[0] == "gpio":
                            pm.show_GPIO_ports()
                            #print("[configuring gpio]:")
                            #print("1. N -> Config new GPIO pin")
                            #print("2. Q -> Quit")
                        else:
                            print(f"{colors.RED}Invalid pin mode{colors.WHITE}")
                    else:
                        print(f"{colors.RED}Invalid number of parameters{colors.WHITE}")
                else:
                    print(f"{colors.RED}Command not found{colors.WHITE}")

    except KeyboardInterrupt:
        print("\n")
    except Exception as e:
        print(f"{colors.RED}Error: {e}{colors.WHITE}")