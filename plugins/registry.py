from .app1.views import firstpage as app1_firstpage
from .app1.views import page2 as app1_page2
from .app1.views import exit as app1_exit

from .app2.views import dashboard as app2_dashboard

"""
This file contains the apps that are token-accessible.
They are registered in views.py.

app2 is authenticated-accessible. 
It is, in addition, registered in apps.py and found in PLUGINS_login:
refer to core.registry.py.
This allows it to appear in the dashboard, home.html, upon logging in:
refer to core/views.py and core/templates/core/home.html.
"""

PLUGIN_REGISTRY = {
    "app1": {
        "firstpage": app1_firstpage,
        "page2": app1_page2,
        "exit": app1_exit,
    },
    "app2": {
        "dashboard": app2_dashboard,
    },
}



from .app3.views import firstpage as app3_firstpage
from .app3.views import page2 as app3_page2
from .app3.views import exit as app3_exit

PLUGIN_REGISTRY |=  {
    "app3": {
        "firstpage": app3_firstpage,
        "page2": app3_page2,
        "exit": app3_exit,
    }
}


"""
# mcqset1
from .mcqset1.views import page1 as mcqset1_page1
from .mcqset1.views import exit as mcqset1_exit

PLUGIN_REGISTRY |=  {
    "mcqset1": {
        "page1": mcqset1_page1,
        "exit": mcqset1_exit,
    }
}
"""

"""
This function allows registering the plugins,
like in the above,
to be done using strings alone - see below.
"""

import importlib

def register_plugin(app_name, function_names):
    """
    app_name: str, e.g. "mcqset1"
    function_names: iterable of str, e.g. ["page1", "exit"]
    """
    module_path = f".{app_name}.views"
    module = importlib.import_module(module_path, package=__package__)

    PLUGIN_REGISTRY[app_name] = {
        fn: getattr(module, fn)
        for fn in function_names
    }


register_plugin(
    app_name="mcqset1",
    function_names=["firstpage", "review", "exit"],
)

register_plugin(
    app_name="mcqset2",
    function_names=["dashboard", "firstpage", "review", "clear", "exit"],
)