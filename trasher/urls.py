"""trasher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from trash_app.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^adminka/$', AdminTrash.as_view(), name='admin-trash'),
    url(r'^adminka/add_marker/$', add_marker, name='add-marker'),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^user-profile/$', user_profile, name='user_profile'),
    url(r'^profile-submit/$', add_date_time, name='profile_submit'),
    url(r'^', include('trash_app.urls', namespace='trash_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

urlpatterns += staticfiles_urlpatterns()
