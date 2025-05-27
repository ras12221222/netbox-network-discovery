# NetBox Network Discovery Plugin

This plugin allows recursive network discovery using CDP and LLDP via SSH, starting from a seed device in NetBox.

## Features

- SSH-based discovery (`show cdp neighbors detail` and `show lldp neighbors detail`)
- Recursive up to N levels deep
- CSV download of discovered devices

## Folder Structure
```
netbox-network-discovery/
├── setup.py
├── README.md
└── netbox_network_discovery/
    ├── __init__.py
    ├── plugin.py
    ├── discovery.py
    ├── urls.py
    └── views.py
```
## Installation

Clone into NetBox local/ directory:
   ```bash
   git clone https://github.com/<REPO> /opt/netbox/local/netbox-network-discovery
   ```

PLUGINS = ['netbox_network_discovery']
```
http://<your-netbox>/plugins/netbox_network_discovery/discover/
```

## Modify the environment variables
```
NETBOX_URL = os.getenv("NETBOX_URL", "http://localhost:8000")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN", "your-token")

USERNAME = os.getenv("SSH_USERNAME", "admin")
PASSWORD = os.getenv("SSH_PASSWORD", "password")
```
