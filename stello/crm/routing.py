from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/crm/figma/order/(?P<author>\d+)/$',
            consumers.FigmaOrderConsumer),
]
