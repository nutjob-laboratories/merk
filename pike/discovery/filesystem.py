import os

EXCLUDED_MODULE_NAMES = ['__init__.py']


def is_package(path):
    """Checks if path string is a package"""
    return os.path.exists(os.path.join(path, '__init__.py'))


def is_module(path):
    """Checks if path string is a module"""
    return path.endswith('.py')


def get_name(path):
    filename = os.path.basename(path)
    name, _ = os.path.splitext(filename)
    return name


def find_modules(path):
    """Finds all modules located on a path"""
    for pathname in os.listdir(path):
        if pathname in EXCLUDED_MODULE_NAMES:
            continue

        full_path = os.path.join(path, pathname)
        if os.path.isfile(full_path) and is_module(full_path):
            yield full_path


def find_packages(path):
    """Finds all packages located on a path"""
    for pathname in os.listdir(path):
        full_path = os.path.join(path, pathname)
        if os.path.isdir(full_path) and is_package(full_path):
            yield full_path


def recursive_find_packages(path):
    """Recursively finds all packages located on a path"""
    for pkg in find_packages(path):
        yield pkg
        for sub_pkg in recursive_find_packages(pkg):
            yield sub_pkg


def recursive_find_modules(path):
    """Recursively finds all modules located on a path"""
    for module_path in find_modules(path):
        yield module_path

    for pkg_path in recursive_find_packages(path):
        for module_path in find_modules(pkg_path):
            yield module_path
