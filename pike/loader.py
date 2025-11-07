import os
import sys
import importlib.util
import importlib.abc


class PikeLoader(importlib.abc.Loader):
    def __init__(self, fullname, module_path):
        self.fullname = fullname
        self.module_path = module_path

    def is_package(self, fullname=None):
        """
        :param fullname: Not used, but required for Python 3.4
        """

        filename = os.path.basename(self.module_path)
        return filename.startswith('__init__')

    def augment_module(self, fullname, module):
        package, _, _ = fullname.rpartition('.')

        if self.is_package():
            module.__path__ = [self.module_path]
            module.__package__ = fullname
        else:
            module.__package__ = package

        return module

    def create_module(self, spec):
        # Use default module creation semantics
        return None

    def exec_module(self, module):
        # Actually execute the code in the module
        with open(self.module_path, 'rb') as f:
            code = compile(f.read(), self.module_path, 'exec')
            exec(code, module.__dict__)

    def load_module(self, fullname):
        if self.fullname != fullname:
            raise ImportError('Cannot import module with this loader')

        if fullname in sys.modules:
            return sys.modules[fullname]

        module = self.load_module_by_path(fullname, self.module_path)
        sys.modules[fullname] = module
        return module

    def load_module_by_path(self, module_name, path):
        _, ext = os.path.splitext(path)
        module = None

        # FIXME(jmvrbanac): Get this working properly in PY3
        # Python 3 - Try to get the cache filename
        # if six.PY3:
        #     compiled_filename = imp.cache_from_source(path)
        #     if os.path.exists(compiled_filename):
        #         path, ext = compiled_filename, '.pyc'

        # if ext.lower() == '.pyc':
        #     module = imp.load_compiled(module_name, path)
        # elif ext.lower() == '.py':
        if ext.lower() == '.py':
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module {module_name} from {path}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module  # <-- This is key!
            spec.loader.exec_module(module)

        if module:
            # Make sure we properly fill-in __path__ and __package__
            module = self.augment_module(module_name, module)

        return module
