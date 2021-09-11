import sys

from pike.discovery import filesystem
from pike.discovery import py
from pike.finder import PikeFinder


class PikeManager(object):
    def __init__(self, search_paths=None):
        """The Pike plugin manager

        The manager allows for the dynamic loading of Python packages for any
        location on a user's filesystem.

        :param list search_paths: List of path strings to include during module
            importing. These paths are only in addition to existing Python
            import search paths.


        Using PikeManager as a context manager:

        .. code-block:: python

            from pike.manager import PikeManager

            with PikeManager(['/path/containing/package']) as mgr:
                import module_in_the_package

        Using PikeManager instance:

        .. code-block:: python

            from pike.manager import PikeManager

            mgr = PikeManager(['/path/container/package'])
            import module_in_the_package
            mgr.cleanup()
        """
        self.search_paths = search_paths or []
        self.module_finder = PikeFinder(search_paths)
        self.add_to_meta_path()

    def cleanup(self):
        """Removes Pike's import hooks

        This should be called if an implementer is not using the manager as
        a context manager.
        """
        if sys.meta_path and self.module_finder in sys.meta_path:
            sys.meta_path.remove(self.module_finder)

    def add_to_meta_path(self):
        """Adds Pike's import hooks to Python

        This should be automatically handled by Pike; however, this is method
        is accessible for very rare use-cases.
        """
        if self.module_finder in sys.meta_path:
            return

        sys.meta_path.insert(0, self.module_finder)

    def get_classes(self, filter_func=None):
        """Get all classes within modules on the manager's search paths

        :param Function filter_func: Custom filter function(cls_obj).
        :returns: :class:`List` of all found classes
        """
        all_classes = []
        # Top-most Modules
        for module_name in self.get_module_names():
            module = py.get_module_by_name(module_name)
            all_classes.extend(py.classes_in_module(module, filter_func))

        # All packages
        for module_name in self.get_package_names():
            module = py.get_module_by_name(module_name)
            all_classes.extend(py.get_all_classes(module, filter_func))

        return all_classes

    def get_all_inherited_classes(self, base_class):
        """Retrieve all inherited classes from manager's search paths

        :param Class base_class: Base class to filter results by
        :return: :class:`List` of all found classes
        """
        all_classes = []
        # Top-most Modules
        for module_name in self.get_module_names():
            module = py.get_module_by_name(module_name)
            all_classes.extend(py.get_inherited_classes(module, base_class))

        # All packages
        for module_name in self.get_package_names():
            module = py.get_module_by_name(module_name)
            inherited = py.get_all_inherited_classes(module, base_class)
            all_classes.extend(inherited)

        return all_classes

    def get_module_names(self):
        """Get root module names available on the manager's search paths

        :returns: :class:`generator` providing available module names.
        """
        for path in self.search_paths:
            for package_path in filesystem.find_modules(path):
                yield filesystem.get_name(package_path)

    def get_package_names(self):
        """Get root package names available on the manager's search paths

        :returns: :class:`generator` providing available package names.
        """
        for path in self.search_paths:
            for package_path in filesystem.find_packages(path):
                yield filesystem.get_name(package_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __del__(self):
        self.cleanup()
