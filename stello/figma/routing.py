from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/figma/product/(?P<id>\d+)/(?P<author_id>\d+)/$',
            consumers.FigmaConsumer),
]
