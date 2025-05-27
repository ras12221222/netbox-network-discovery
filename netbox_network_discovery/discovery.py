import os
import pynetbox
from netmiko import ConnectHandler

NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN", "your-token")

USERNAME = os.getenv("SSH_USERNAME", "admin")
PASSWORD = os.getenv("SSH_PASSWORD", "password")

nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)

COMMAND_MAP = {
    "cisco": [
        "show lldp neighbors detail",
        "show cdp neighbors detail"
    ],
    "juniper": [
        "show lldp neighbors detail"
    ]
}

discovered = set()
results = []

def get_connection_info(device):
    primary_ip = device.primary_ip4 or device.primary_ip6
    if not primary_ip:
        return None
    return {
        'device_type': 'cisco_ios',
        'ip': primary_ip.address.split('/')[0],
        'username': USERNAME,
        'password': PASSWORD,
        'secret': PASSWORD,
    }

def parse_neighbors(output):
    neighbors = []
    for line in output.splitlines():
        if "Management Address" in line or "IP address" in line:
            ip = line.split()[-1]
            neighbors.append(ip)
    return neighbors

def run_discovery(start_device, max_depth=2, depth=0, parent=None):
    global discovered, results
    if depth > max_depth or start_device in discovered:
        return results

    device = nb.dcim.devices.get(name=start_device)
    if not device:
        return results

    discovered.add(start_device)

    conn_info = get_connection_info(device)
    if not conn_info:
        return results

    try:
        conn = ConnectHandler(**conn_info)
        conn.enable()

        vendor = device.device_type.manufacturer.name.lower() if device.device_type else "unknown"
        commands = COMMAND_MAP.get(vendor, [])

        neighbors = []
        for cmd in commands:
            try:
                output = conn.send_command(cmd)
                neighbors += parse_neighbors(output)
            except Exception:
                continue

        results.append({
            "Hostname": device.name,
            "IP": conn_info['ip'],
            "Vendor": vendor,
            "Discovered From": parent if parent else "ROOT",
            "Depth": depth
        })

        for neighbor_ip in set(neighbors):
            nb_device = nb.dcim.devices.filter(primary_ip=neighbor_ip)
            neighbor_name = nb_device[0].name if nb_device else neighbor_ip
            run_discovery(neighbor_name, max_depth, depth + 1, parent=device.name)

    except Exception as e:
        results.append({
            "Hostname": device.name,
            "IP": conn_info['ip'],
            "Vendor": "Unknown",
            "Discovered From": parent if parent else "ROOT",
            "Depth": depth,
            "Error": str(e)
        })

    return results
