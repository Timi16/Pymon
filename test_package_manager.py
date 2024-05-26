
import unittest
from package_manager import install_package, uninstall_package, list_installed_packages, read_installed_packages, write_installed_packages

class TestPackageManager(unittest.TestCase):
    def setUp(self):
        self.original_packages = read_installed_packages()
        write_installed_packages({})

    def tearDown(self):
        write_installed_packages(self.original_packages)

    def test_install_package(self):
        install_package('requests')
        installed_packages = read_installed_packages()
        self.assertIn('requests', installed_packages)

    def test_uninstall_package(self):
        install_package('requests')
        uninstall_package('requests')
        installed_packages = read_installed_packages()
        self.assertNotIn('requests', installed_packages)

    def test_list_installed_packages(self):
        install_package('requests')
        install_package('flask')
        list_installed_packages()

if __name__ == '__main__':
    unittest.main()
