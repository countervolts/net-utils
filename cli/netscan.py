import concurrent.futures
import tqdm
import subprocess

def ping_ip(ip):
    result = subprocess.run(['ping', '-n', '1', '-w', '100', ip], capture_output=True, text=True)
    if "Reply from" in result.stdout:
        return ip
    return None

def netscan(file=None):
    print("Scanning network for users...")
    users_count = 0
    base_ip = "192.168.1."
    ips = [base_ip + str(i) for i in range(1, 255)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(ping_ip, ips), total=len(ips), desc="Scanning IPs"))
    
    for ip in results:
        if ip:
            users_count += 1
            if file:
                file.write(f"Active IP: {ip}\n")
    
    print(f"netscan return with: {users_count}")
    return users_count