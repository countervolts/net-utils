import os
import sys

from cli.inter import off_wifi, off_ethernet, change_mac
from cli.debug import debug
from cli.netscan import netscan
from colorama import init, Fore, Style
from misc.ascii_art import NETCLI_ASCII_ART, ASCII_ART

init()

DEBUG_FILE = "debug_info.txt"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    lines = text.split('\n')
    for line in lines:
        print(line.center(os.get_terminal_size().columns))

def open_config():
    os.system(f'notepad.exe config.py')

def rerun_command_line(with_console=False):
    python = sys.executable
    if with_console:
        os.execv(python, [python, "main.py", "-c", "return_to_menu"])
    else:
        os.execv(python, [python, "main.py"])

def command_line_interface(return_to_menu=False):
    clear_console()
    print_centered(NETCLI_ASCII_ART)
    while True:
        command = input("netutils> ").strip().lower()
        if command == "help" or command == "cmds":
            print("Available commands:")
            print("  help    - Display this help message")
            print("  cmds    - Display this help message")
            print("  values  - Open config.py")
            print("  debug   - Print debug information")
            print("  newmac  - Change MAC address")
            print("  nowifi  - Turn off WiFi")
            print("  noether - Turn off Ethernet")
            print("  netscan - Scan the network for users")
            print("  rerun   - Rerun the main.py script")
            print("           -c option will rerun into the console")
            print("  return  - Return to the main menu")
            print("  clear   - Clear the console")
        elif command == "values":
            open_config()
        elif command == "debug":
            debug()
        elif command == "newmac":
            print(change_mac())
        elif command == "nowifi":
            print(off_wifi())
        elif command == "noether":
            print(off_ethernet())
        elif command == "netscan":
            netscan()
        elif command == "rerun -c":
            rerun_command_line(with_console=True)
        elif command == "rerun":
            rerun_command_line()
        elif command == "clear":
            clear_console()
            print_centered(NETCLI_ASCII_ART)
        elif command == "return":
            if return_to_menu:
                return
            else:
                clear_console()
                print_centered(ASCII_ART)
                return
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")

if __name__ == "__main__":
    return_to_menu = len(sys.argv) > 2 and sys.argv[2] == "return_to_menu"
    command_line_interface(return_to_menu)