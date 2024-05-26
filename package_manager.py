
import os
import json
import requests
import shutil

PACKAGES_DIR = 'packages'
INSTALLED_PACKAGES_FILE = 'installed_packages.json'
METADATA_URL = 'https://pypi.org/pypi/{package}/json'

def fetch_package_metadata(package_name):
    response = requests.get(METADATA_URL.format(package=package_name))
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Package {package_name} not found")

def download_package(package_name, version):
    metadata = fetch_package_metadata(package_name)
    if version not in metadata['releases']:
        raise ValueError(f"Version {version} not found for package {package_name}")

    release = metadata['releases'][version][0]
    package_url = release['url']

    response = requests.get(package_url)
    if response.status_code == 200:
        package_path = os.path.join(PACKAGES_DIR, f'{package_name}-{version}.tar.gz')
        with open(package_path, 'wb') as file:
            file.write(response.content)
        return package_path
    else:
        raise ValueError(f"Failed to download package {package_name} version {version}")

def read_installed_packages():
    if os.path.exists(INSTALLED_PACKAGES_FILE):
        with open(INSTALLED_PACKAGES_FILE, 'r') as file:
            return json.load(file)
    return {}

def write_installed_packages(packages):
    with open(INSTALLED_PACKAGES_FILE, 'w') as file:
        json.dump(packages, file)

def install_package(package_name):
    installed_packages = read_installed_packages()
    if package_name in installed_packages:
        print(f'{package_name} is already installed.')
        return

    os.makedirs(PACKAGES_DIR, exist_ok=True)
    metadata = fetch_package_metadata(package_name)
    latest_version = metadata['info']['version']
    package_info = metadata['info']
    dependencies = package_info.get('requires_dist', [])

    for dep in dependencies:
        dep_name, _, dep_version = dep.partition(' ')
        if dep_name not in installed_packages:
            install_package(dep_name)

    package_path = download_package(package_name, latest_version)
    installed_packages[package_name] = latest_version
    write_installed_packages(installed_packages)
    print(f'Package {package_name} version {latest_version} downloaded to {package_path}')


def uninstall_package(package_name):
    installed_packages = read_installed_packages()
    if package_name not in installed_packages:
        print(f'{package_name} is not installed.')
        return

    version = installed_packages.pop(package_name)
    package_path = os.path.join(PACKAGES_DIR, f'{package_name}-{version}.tar.gz')

    if os.path.exists(package_path):
        os.remove(package_path)
        print(f'Removed {package_name} version {version} from {package_path}')
    else:
        print(f'Package {package_name} not found in the expected directory.')

    write_installed_packages(installed_packages)
    print(f'Package {package_name} uninstalled successfully.')

def list_installed_packages():
    installed_packages = read_installed_packages()
    if not installed_packages:
        print('No packages installed.')
    else:
        print('Installed packages:')
        for package, version in installed_packages.items():
            print(f'{package}=={version}')
