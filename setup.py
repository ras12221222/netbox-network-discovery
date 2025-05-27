from setuptools import setup, find_packages

setup(
    name='netbox-network-discovery',
    version='0.1',
    description='NetBox plugin for recursive network discovery',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
