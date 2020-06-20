"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from . import page
from . import gesture
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/device1', page.device1),
    path('users/device2', page.device2),
    path('wsapi/', include('wsapi.urls')),
    path('users/gesturemsgoffline',gesture.gesturemsgoffline),
    path('users/finedata',gesture.finedata),
    path('users/parameters', gesture.parametersreq),
    path('users/rtfinedata', gesture.finedatareq),
    path('users/fftonline', gesture.fftonline)
]
