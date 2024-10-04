import subprocess

def change_mac():
    try:
        result = subprocess.run('getmac', capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        mac_address = result.stdout.split()[0]
        new_mac = "02:00:00:" + ":".join(mac_address.split(":")[3:])
        result = subprocess.run(f'netsh interface set interface "Wi-Fi" newmac={new_mac}', capture_output=True, text=True)
        if result.returncode == 0:
            return f"Success - Changed MAC address from {mac_address} to {new_mac}"
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"