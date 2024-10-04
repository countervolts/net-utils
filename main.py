import os
import subprocess
import socket
import psutil
import sys
import ctypes
from misc.ascii_art import ASCII_ART
from misc.commands import undo_commands, wifi_commands, ethernet_commands
from commandline import command_line_interface
from colours import COLOR_1, COLOR_2, COLOR_3, COLOR_4, COLOR_5, RESET

TRACK_FILE = "status"
LOG_FILE = "log.txt"

def has_perms():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def permission_giver():
    try:
        script_path = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    except Exception as e:
        input(f"Problem with giving permissions: {e}")

def supports_jumbo_packets(interface):
    result = subprocess.run(f'netsh interface ipv4 show subinterfaces | findstr /C:"{interface}"', shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return False
    output = result.stdout.strip()
    mtu_value = int(output.split()[-2])
    return mtu_value >= 9000

def run_commands(commands, interface):
    command_status = ["pending"] * len(commands)
    jumbo_supported = supports_jumbo_packets(interface)
    with open(LOG_FILE, 'w') as log_file:
        for i, (description, command) in enumerate(commands):
            if "jumbo packets" in description.lower() and not jumbo_supported:
                command_status[i] = "unavailable"
                continue
            command_status[i] = "running"
            clear_console()
            list_commands(commands, command_status)
            log_file.write(f"Running: {description}\n")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            log_file.write(result.stdout)
            log_file.write(result.stderr)
            command_status[i] = "done"
            clear_console()
            list_commands(commands, command_status)
    if not jumbo_supported:
        print(f"{COLOR_4}Note: Jumbo packets are not supported on this interface. Skipping related commands.{RESET}")

def list_commands(commands, command_status):
    for i, (description, _) in enumerate(commands):
        if command_status[i] == "pending":
            status = COLOR_1
        elif command_status[i] == "running":
            status = COLOR_2
        elif command_status[i] == "unavailable":
            status = COLOR_3
        else:
            status = COLOR_4
        print(f"{status}{i + 1}. {description}{RESET}")

def toggle_command(commands, commands_status):
    while True:
        list_commands(commands, commands_status)
        choice = input("Enter the number of the command to enable/disable (or 'exit' to go back): ")
        clear_console()
        if choice.lower() == 'exit':
            break
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(commands_status):
                commands_status[index] = not commands_status[index]
            else:
                print("Invalid choice.")
        else:
            print("Invalid input.")

def get_active_connection():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and psutil.net_if_stats()[interface].isup:
                if "Wi-Fi" in interface or "Wireless" in interface:
                    return "wifi"
                elif "Ethernet" in interface:
                    return "ethernet"
    return None

def print_centered(text):
    lines = text.split('\n')
    for line in lines:
        print(line.center(os.get_terminal_size().columns))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_centered(ASCII_ART)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        return

    if not has_perms():
        permission_giver()
        return 

    clear_console()
    
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'r') as file:
            status = file.read().strip()
    else:
        status = "not optimized"

    active_connection = get_active_connection()
    if active_connection == "wifi":
        commands = wifi_commands
    elif active_connection == "ethernet":
        commands = ethernet_commands
    else:
        input("No active WiFi or Ethernet connection detected. (offline?)")
        return

    commands_status = [True] * len(commands)

    while True:
        print_centered("1. Optimize WiFi Connections" if active_connection == "wifi" else "1. Optimize Ethernet Connections")
        print_centered("2. Undo Optimizations")
        print_centered("3. List/Toggle Commands")
        print_centered("4. Switch to Ethernet" if active_connection == "wifi" else "4. Switch to WiFi")
        print_centered("5. Command Line Interface")
        print()
        choice = input("Choose an option: ")
        clear_console()

        if choice == "1":
            enabled_commands = [cmd for cmd, enabled in zip(commands, commands_status) if enabled]
            print(f"{len(enabled_commands)}/{len(commands)} commands will run.")
            if status == "true":
                input("Connections are already optimized. (enter to continue)")
            else:
                run_commands(enabled_commands, active_connection)
                with open(TRACK_FILE, 'w') as file:
                    file.write("optimized")
                input("Connections have been optimized. (enter to continue)")
                clear_console()
        elif choice == "2":
            if status == "not optimized":
                input("Optimization has not run yet. (enter to continue)")
                clear_console()
            else:
                run_commands(undo_commands, active_connection)
                os.remove(TRACK_FILE)
                input("Optimizations have been undone. (enter to continue)")
                clear_console()
        elif choice == "3":
            toggle_command(commands, commands_status)
        elif choice == "4":
            active_connection = "ethernet" if active_connection == "wifi" else "wifi"
            commands = ethernet_commands if active_connection == "ethernet" else wifi_commands
            commands_status = [True] * len(commands)
        elif choice == "5":
            command_line_interface()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()