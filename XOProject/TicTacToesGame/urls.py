from django.urls import path, re_path
from django.conf.urls import include
from .views import TicTacAPI

websocket_urlpatterns = [
    # path("game/", TicTacAPI, name="TicTacToeAPI"),
    re_path(r'^ws/play/(?P<room_id>\w+)/$', TicTacAPI.as_asgi())
]