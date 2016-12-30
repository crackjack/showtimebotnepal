from django.conf.urls import include, url
from .views import BotView
urlpatterns = [
                  url(r'^yobotyo/?$', BotView.as_view()) 
               ]
