from extras.plugins import PluginConfig

class NetworkDiscoveryConfig(PluginConfig):
    name = 'netbox_network_discovery'
    verbose_name = 'Network Discovery'
    description = 'Recursively discovers devices from NetBox using CDP/LLDP'
    version = '0.1'
    author = 'Rassul Ismailov'
    author_email = '1222ras1222@gmail.com'

config = NetworkDiscoveryConfig
