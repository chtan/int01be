from django.http import Http404
from .registry import PLUGIN_REGISTRY

def plugin_dispatch(request, plugin, action):
    try:
        handler = PLUGIN_REGISTRY[plugin][action]
    except KeyError:
        raise Http404("Plugin or action not found")

    return handler(request)
