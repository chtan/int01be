from .app1.views import firstpage as app1_firstpage
from .app1.views import page2 as app1_page2
from .app1.views import exit as app1_exit

from .app2.views import dashboard as app2_dashboard

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