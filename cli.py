
import argparse
from package_manager import install_package, uninstall_package, list_installed_packages

def main():
    parser = argparse.ArgumentParser(description='My Package Manager')
    parser.add_argument('command', choices=['install', 'uninstall', 'list'], help='Command to run')
    parser.add_argument('package', nargs='?', help='Package to install/uninstall')

    args = parser.parse_args()

    if args.command == 'install':
        install_package(args.package)
    elif args.command == 'uninstall':
        uninstall_package(args.package)
    elif args.command == 'list':
        list_installed_packages()

if __name__ == '__main__':
    main()
