from django.apps import AppConfig


class PluginsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins'

    authenticated_apps = [
        'app2',
        ##ENTER_APP_HERE
    ]

    def ready(self):
        from core.registry import register_plugin_login
        
        for app in self.authenticated_apps:
            register_plugin_login(app, self)


