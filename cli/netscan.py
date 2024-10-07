import concurrent.futures
import tqdm
import subprocess
import os
from scapy.all import ARP, Ether, srp
import nmap

def ping_ip(ip):
    result = subprocess.run(['ping', '-n', '1', '-w', '100', ip], capture_output=True, text=True)
    if "Reply from" in result.stdout:
        return ip
    return None

def get_mac_address(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    return "N/A"

def get_os(ip):
    nm = nmap.PortScanner()
    try:
        nm.scan(ip, arguments='-O')
        if 'osclass' in nm[ip]:
            for osclass in nm[ip]['osclass']:
                return osclass['osfamily']
        elif 'osmatch' in nm[ip]:
            return nm[ip]['osmatch'][0]['name']
    except Exception as e:
        return f"Error: {str(e)}"
    return "Unknown"

def netscan(log_file=None, get_mac=False, get_os_flag=False):
    print("Scanning network for users...")
    users_count = 0
    base_ip = "192.168.1."
    ips = [base_ip + str(i) for i in range(1, 255)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm.tqdm(executor.map(ping_ip, ips), total=len(ips), desc="Scanning IPs"))
    
    if log_file:
        with open(log_file, 'w') as file:
            for ip in results:
                if ip:
                    users_count += 1
                    mac_address = get_mac_address(ip) if get_mac else "N/A"
                    os_info = get_os(ip) if get_os_flag else "Unknown"
                    file.write(f"Active IP: {ip}, MAC Address: {mac_address}, OS: {os_info}\n")
    else:
        for ip in results:
            if ip:
                users_count += 1
                mac_address = get_mac_address(ip) if get_mac else "N/A"
                os_info = get_os(ip) if get_os_flag else "Unknown"
                print(f"Active IP: {ip}, MAC Address: {mac_address}, OS: {os_info}")
    
    print(f"netscan return with: {users_count} users online")
    return users_count