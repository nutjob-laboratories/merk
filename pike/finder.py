import os

from pike import loader


class PikeFinder(object):
    def __init__(self, paths=None):
        self.paths = paths or []

    def module_name_to_filename(self, fullname):
        separated_name = fullname.split('.')
        return os.path.join(*separated_name)

    def get_import_filename(self, module_path):
        for base_path in self.paths:
            target_path = os.path.join(base_path, module_path)
            is_pkg = os.path.isdir(target_path)

            if is_pkg:
                filename = os.path.join(target_path, '__init__.py')
            else:
                filename = '{}.py'.format(target_path)

            if os.path.exists(filename):
                return filename

    def find_module(self, fullname, path=None):
        converted_name = self.module_name_to_filename(fullname)
        module_path = self.get_import_filename(converted_name)

        if module_path:
            return loader.PikeLoader(fullname, module_path)
