from config import MTU_VALUE, WI_FI_METRIC_HIGH, WI_FI_METRIC_LOW, ETHERNET_METRIC_HIGH, ETHERNET_METRIC_LOW

commands = [
    ("Flushing DNS", "ipconfig /flushdns"),
    ("Releasing IP Address", "ipconfig /release"),
    ("Renewing IP Address", "ipconfig /renew"),
    ("Resetting TCP/IP Stack", "netsh int ip reset"),
    ("Resetting Winsock", "netsh winsock reset"),
    ("Disabling TCP Auto-Tuning", "netsh interface tcp set global autotuninglevel=disabled"),
    ("Disabling Network Throttling", "reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"),
    ("Enabling Large Send Offload", "netsh int tcp set global rsc=enabled")
]

wifi_commands = [
    ("Flushing DNS", "ipconfig /flushdns"),
    ("Releasing IP Address", "ipconfig /release"),
    ("Renewing IP Address", "ipconfig /renew"),
    ("Resetting TCP/IP Stack", "netsh int ip reset"),
    ("Resetting Winsock", "netsh winsock reset"),
    ("Disabling TCP Auto-Tuning", "netsh interface tcp set global autotuninglevel=disabled"),
    ("Disabling Network Throttling", "reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"),
    ("Enabling Large Send Offload", "netsh int tcp set global rsc=enabled"),
    (f"Setting MTU to {MTU_VALUE}", f"netsh interface ipv4 set subinterface \"Wi-Fi\" mtu={MTU_VALUE} store=persistent"),
    (f"Making Ethernet less prioritized", f"netsh interface ipv4 set interface \"Ethernet\" metric={ETHERNET_METRIC_LOW}"),
    (f"Making Wi-Fi more prioritized", f"netsh interface ipv4 set interface \"Wi-Fi\" metric={WI_FI_METRIC_HIGH}")
]

wifi_undo_commands = [
    ("Enabling TCP Auto-Tuning", "netsh interface tcp set global autotuninglevel=normal"),
    ("Enabling Network Throttling", "reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f"),
    ("Disabling Large Send Offload", "netsh int tcp set global rsc=disabled"),
    (f"Resetting MTU for Wi-Fi", f"netsh interface ipv4 set subinterface \"Wi-Fi\" mtu=1500 store=persistent"),
    (f"Resetting Ethernet priority", f"netsh interface ipv4 set interface \"Ethernet\" metric=25"),
    (f"Resetting Wi-Fi priority", f"netsh interface ipv4 set interface \"Wi-Fi\" metric=25")
]

ethernet_commands = [
    ("Flushing DNS", "ipconfig /flushdns"),
    ("Releasing IP Address", "ipconfig /release"),
    ("Renewing IP Address", "ipconfig /renew"),
    ("Resetting TCP/IP Stack", "netsh int ip reset"),
    ("Resetting Winsock", "netsh winsock reset"),
    ("Disabling TCP Auto-Tuning", "netsh interface tcp set global autotuninglevel=disabled"),
    ("Disabling Network Throttling", "reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"),
    ("Enabling Large Send Offload", "netsh int tcp set global rsc=enabled"),
    (f"Setting MTU to {MTU_VALUE}", f"netsh interface ipv4 set subinterface \"Ethernet\" mtu={MTU_VALUE} store=persistent"),
    (f"Making Wi-Fi less prioritized", f"netsh interface ipv4 set interface \"Wi-Fi\" metric={WI_FI_METRIC_LOW}"),
    (f"Making Ethernet more prioritized", f"netsh interface ipv4 set interface \"Ethernet\" metric={ETHERNET_METRIC_HIGH}")
]

ethernet_undo_commands = [
    ("Enabling TCP Auto-Tuning", "netsh interface tcp set global autotuninglevel=normal"),
    ("Enabling Network Throttling", "reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f"),
    ("Disabling Large Send Offload", "netsh int tcp set global rsc=disabled"),
    (f"Resetting MTU for Ethernet", f"netsh interface ipv4 set subinterface \"Ethernet\" mtu=1500 store=persistent"),
    (f"Resetting Wi-Fi priority", f"netsh interface ipv4 set interface \"Wi-Fi\" metric=25"),
    (f"Resetting Ethernet priority", f"netsh interface ipv4 set interface \"Ethernet\" metric=25")
]