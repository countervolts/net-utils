import os
import sys
import json
import subprocess
import keyboard
from cli.inter import change_mac
from cli.debug import debug
from cli.netscan import netscan
from misc.ascii_art import NETCLI_ASCII_ART, ASCII_ART
from colours import COLOR_1, COLOR_2, COLOR_3, COLOR_4, RESET

DEBUG_FILE = "debug_info.txt"
CUSTOM_COMMANDS_FILE = "custom_commands.json"

CORE_COMMANDS = [
    "help", "cmds", "values", "debug", "netscan", "rerun", "return", "clear", "create", "delete", "dumpdrivers", "newmac"
]

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
        os.execv(python, [python, "main.py", "-c"])
    else:
        os.execv(python, [python, "main.py"])

def load_custom_commands():
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        with open(CUSTOM_COMMANDS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_custom_commands(commands):
    with open(CUSTOM_COMMANDS_FILE, 'w') as file:
        json.dump(commands, file, indent=4)

def create_custom_command(custom_commands):
    name = input("Command name: ").strip().lower()
    cmd = input("Command: ").strip()
    about = input("Command about: ").strip()
    custom_commands[name] = {"command": cmd, "about": about}
    save_custom_commands(custom_commands)
    print(f"{COLOR_3}Custom command '{name}' added successfully!{RESET}")
    print("Run 'help' to see changes.")

def dump_drivers():
    try:
        output_file = "network_drivers.txt"
        with open(output_file, 'w') as file:
            print("Dumping Wi-Fi drivers...")
            file.write("Wi-Fi Drivers:\n")
            result = subprocess.run('netsh wlan show drivers', shell=True, capture_output=True, text=True)
            file.write(result.stdout)
            
            print("Dumping Ethernet drivers...")
            file.write("\nEthernet Drivers:\n")
            result = subprocess.run('netsh lan show drivers', shell=True, capture_output=True, text=True)
            file.write(result.stdout)
        
        print(f"Network drivers dumped to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_command_suggestions(text):
    return [cmd for cmd in CORE_COMMANDS if cmd.startswith(text)]


def command_line_interface(return_to_menu=False):
    clear_console()
    print_centered(NETCLI_ASCII_ART)
    custom_commands = load_custom_commands()
    
    while True:
        command = input("netutils> ").strip().lower()
        
        if keyboard.is_pressed('tab'):
            suggestions = get_command_suggestions(command)
            if suggestions:
                print(f"\nSuggestions: {', '.join(suggestions)}")
                command = suggestions[0]
        
        if command == "help" or command == "cmds":
            print(f"{COLOR_1}Core commands:{RESET}")
            print(f"  {COLOR_2}help/cmds{RESET}    - Display this help message")
            print(f"  {COLOR_2}debug{RESET}   - Print debug information")
            print(f"  {COLOR_2}netscan{RESET} - Scan the network for users")
            print(f"  {COLOR_2}rerun{RESET}   - Rerun the main.py script")
            print(f"             -c option will rerun into the console\n")
            print(f"  {COLOR_2}create{RESET}  - Create a custom command")
            print(f"  {COLOR_2}delete{RESET}  - Delete a custom command")
            print(f"{COLOR_1}\nAdditional commands:{RESET}")
            print(f"  {COLOR_2}newmac{RESET}  - Change MAC address")
            print(f"  {COLOR_2}values{RESET}  - Open config.py")
            print(f"  {COLOR_2}return{RESET}  - Return to the main menu")
            print(f"  {COLOR_2}clear{RESET}   - Clear the console")            
            for name, details in custom_commands.items():
                print(f"  {COLOR_2}{name}{RESET} - {details['about']}")
        elif command == "values":
            open_config()
        elif command == "debug":
            debug()
        elif command == "newmac":
            print(change_mac())
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
        elif command == "create":
            create_custom_command(custom_commands)
        elif command == "delete":
            if not custom_commands:
                print(f"{COLOR_4}No custom commands to delete!{RESET}")
            else:
                name = input("Command name to delete: ").strip().lower()
                if name in custom_commands:
                    del custom_commands[name]
                    save_custom_commands(custom_commands)
                    print(f"{COLOR_3}Custom command '{name}' deleted successfully!{RESET}")
                    print("Run 'help' to see changes.")
                else:
                    print(f"{COLOR_4}Custom command '{name}' not found!{RESET}")
        elif command in custom_commands:
            os.system(custom_commands[command]["command"])
        else:
            print(f"{COLOR_4}Unknown command: {command}{RESET}")

if __name__ == "__main__":
    return_to_menu = len(sys.argv) > 1 and sys.argv[1] == "-c"
    command_line_interface(return_to_menu)