#PLUGINS = {}
#
#def register_plugin(name, app_config):
#    """Register plugin app"""
#    PLUGINS[name] = app_config
#
#def get_plugin_urls():
#    """Return a list of URL namespaces for installed plugins"""
#    return [cfg.label for cfg in PLUGINS.values()]


PLUGINS_login = {}

def register_plugin_login(name, app_config):
    """Register plugin app"""
    PLUGINS_login[name] = app_config

def get_plugin_login_urls():
    """Return a list of URL namespaces for installed plugins"""
    return [cfg.label for cfg in PLUGINS_login.values()]


#PLUGINS_token = {}
#
#def register_plugin_token(name, app_config):
#    """Register plugin app"""
#    PLUGINS_token[name] = app_config
#
#def get_plugin_token_urls():
#    """Return a list of URL namespaces for installed plugins"""
#    return [cfg.label for cfg in PLUGINS_token.values()]
