# chat/routing.py
from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'wsapi/api/(?P<api_name>\w+)/$', consumers.APIConsumer),
]