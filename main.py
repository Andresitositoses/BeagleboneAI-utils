from src.pinsManager import PinsManager
import src.pinsManager as pinsManager
import src.colors as colors

pm = PinsManager()

def help():
    
    # Clean the screen
    print("\033c\n\n\n\n", end="")

    print(" " * pinsManager.MARGIN_SHOW + f"{colors.BLUE}##################################")
    print(" " * pinsManager.MARGIN_SHOW + "##      Available commands      ##")
    print(" " * pinsManager.MARGIN_SHOW + "##################################\n")
    print(" " * pinsManager.MARGIN_SHOW + " - show all [--one-column]")
    print(" " * pinsManager.MARGIN_SHOW + " - show [type1] [type2] [typeN] [--one-column]")
    print(" " * pinsManager.MARGIN_SHOW + " - configure <pin-mode>")
    print(" " * pinsManager.MARGIN_SHOW + " - clear")
    print(f"{colors.WHITE}\n")

# Main program consists of a loop that waits for user input commands
if __name__ == "__main__":

    # Show the help
    help()

    while True:
        try:
            command = input(f"{colors.GREEN}PinsManager> {colors.WHITE}")
            if command == "exit":
                break
            elif command == "help":
                help()
            elif "show" in command:
                command = command.replace("show", "").strip()
                # Parse the command
                spec_format = pinsManager.ONE_COLUMN_FORMAT if "--one-column" in command else pinsManager.TWO_COLUMNS_FORMAT
                command = command.replace("--one-column", "")
                if "all" in command:
                    pm.show_pinout(format=spec_format)
                else:
                    pm.show_pinout(format=spec_format,filtered_pins=command.upper().split(" "))
            # elif "configure" in command:
                # if "gpio" in command:
            elif command == "clear" or command == "cls":
                command = command.replace("clear", "").replace("cls", "")
                print("\033c\n\n\n\n", end="")
            else:
                print(f"{colors.RED}Command not found{colors.WHITE}")

        except KeyboardInterrupt:
            print("\n")
        except Exception as e:
            print(f"{colors.RED}Error: {e}{colors.WHITE}")