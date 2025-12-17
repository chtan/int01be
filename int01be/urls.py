"""
URL configuration for int01be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simple1/', include('simple1.urls')),
    path('simple2/', include('simple2.urls')),
]

urlpatterns += [path('simple3/', include('simple3.urls'))]
urlpatterns += [path('simple4/', include('simple4.urls'))]

urlpatterns += [path('simple5/', include('simple5.urls'))]
urlpatterns += [path('simple6/', include('simple6.urls'))]

urlpatterns += [path('core/', include('core.urls'))]

# Dynamically include plugins
#
# Namespaces cannot be added dynamically, need server to restart.
# Urls, though, can be added dynamically.
#

# _login : plugins available for logged-in users.
# _token : plugins available for token-based users.

"""
for plugin_config in PLUGINS.values():
    try:
        urlpatterns.append(
            path(f'core/{plugin_config.name}/', include(f"{plugin_config.name}.urls", namespace=plugin_config.label))
        )
    except ModuleNotFoundError:
        # Skip if plugin has no urls.py
        pass
"""
urlpatterns += [path('plugins/', include('plugins.urls'))]


#
# I had to do this to allow css to be detected by both localhost and 127.0.0.1,
# together with some configurations in settings.py.
#
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)