import os
import subprocess

DEBUG_FILE = "debug_info.txt"

def debug():
    os.system('title netutils (dbg)')
    with open(DEBUG_FILE, 'w') as file:
        print("Gathering debug information...")
        file.write("Gathering debug information...\n")
        
        print("Getting Device Information...")
        file.write("Device Information:\n")
        result = subprocess.run('systeminfo', shell=True, capture_output=True, text=True)
        file.write(result.stdout)
        
        print("Getting Network Information...")
        file.write("\nNetwork Information:\n")
        result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True)
        file.write(result.stdout)
        
        print("Getting WiFi Information...")
        file.write("\nWiFi Information:\n")
        result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
        file.write(result.stdout)
        
        print("Getting Ethernet Information...")
        file.write("\nEthernet Information:\n")
        result = subprocess.run('netsh interface show interface', shell=True, capture_output=True, text=True)
        file.write(result.stdout)
        
        print("Getting Router Information...")
        file.write("\nRouter Information:\n")
        result = subprocess.run('tracert -d 8.8.8.8', shell=True, capture_output=True, text=True)
        file.write(result.stdout)
        
    print(f"Debug information written to {DEBUG_FILE}")