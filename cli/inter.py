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
            return "Ok."
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def off_wifi():
    try:
        result = subprocess.run('netsh interface set interface "Wi-Fi" admin=disable', capture_output=True, text=True)
        if result.returncode == 0:
            return "Ok."
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def off_ethernet():
    try:
        result = subprocess.run('netsh interface set interface "Ethernet" admin=disable', capture_output=True, text=True)
        if result.returncode == 0:
            return "Ok."
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"