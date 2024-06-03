import importlib

def load_plugin(plugin_name):
    module = importlib.import_module(plugin_name)
    if hasattr(module, 'init'):
        module.init()
