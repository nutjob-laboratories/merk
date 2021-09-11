import os
import importlib
import inspect

from pike.discovery import filesystem


def get_module_by_name(full_module_name):
    """Import module by full name

    :param str full_module_name: Full module name e.g. (pike.discovery.py)
    :return: Imported :class:`module`
    """
    return importlib.import_module(full_module_name)


def is_child_of_module(obj, parent):
    package, _, name = obj.__name__.rpartition('.')
    return package.startswith(parent.__name__)


def _import_from_path(path, package_name):
    module_name = filesystem.get_name(path)
    fullname = '{}.{}'.format(package_name, module_name)

    return get_module_by_name(fullname)


def _child_modules(module):
    package_path = os.path.dirname(inspect.getabsfile(module))

    # Import all child modules
    for module_path in filesystem.find_modules(package_path):
        _import_from_path(module_path, module.__package__ or module.__name__)

    # Import all sub packages
    for package_path in filesystem.find_packages(package_path):
        _import_from_path(package_path, module.__package__ or module.__name__)

    for name, obj in inspect.getmembers(module):
        if inspect.ismodule(obj) and is_child_of_module(obj, module):
            yield obj


def classes_in_module(module, filter_func=None):
    """Retrieve classes within a module

    :param module module: Module to search under
    :param Function filter_func: Custom filter function(cls_obj).
    :return: :class:`generator` containing classes within a module
    """
    finder_filter = filter_func or (lambda x: True)

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and finder_filter(obj):
            yield obj


def get_inherited_classes(module, base_class):
    """Retrieve inherited classes from a single module

    :param module module: Module to search under
    :param Class base_class: Base class to filter results by
    :return: :class:`List` of all found classes
    """
    def class_filter(cls):
        return cls != base_class and issubclass(cls, base_class)

    return list(classes_in_module(module, class_filter))


def get_child_modules(module, recursive=True):
    """Retrieve child modules

    :param module module: Module to search under
    :param bool recursive: Toggles the retrieval of sub-children module.
    :return: :class:`generator` containing child modules
    """
    for child_module in _child_modules(module):
        yield child_module

        if recursive:
            for sub_child_module in _child_modules(child_module):
                yield sub_child_module


def get_all_classes(module, filter_func=None):
    """Retrieve all classes from modules

    :param module module: Module to search under
    :param Function filter_func: Custom filter function(cls_obj).
    :returns: :class:`List` of all found classes
    """
    all_classes = []

    # Current module's classes
    all_classes.extend([cls for cls in classes_in_module(module, filter_func)])

    # All child module classes
    for child_module in get_child_modules(module):
        child_module_classes = classes_in_module(child_module, filter_func)
        all_classes.extend([cls for cls in child_module_classes])

    # TODO(jmvrbanac): Rework this so that we don't have to use a set
    return list(set(all_classes))


def get_all_inherited_classes(module, base_class):
    """Retrieve all inherited classes from modules

    :param module module: Module to search under
    :param Class base_class: Base class to filter results by
    :return: :class:`List` of all found classes
    """
    def class_filter(cls):
        return cls != base_class and issubclass(cls, base_class)

    return get_all_classes(module, class_filter)
