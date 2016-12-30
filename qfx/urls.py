"""qfx URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from movies.models import Movie
from showtimes.models import Showtime

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'poster', 'trailer', 'plot', 'status')

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.recent.all()
    serializer_class = MovieSerializer

class ShowtimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Showtime
        fields = ('date', 'movie', 'cinema', 'time', 'booking_url')

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer


router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'showtimes', ShowtimeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^~bot/', include('bot.urls')),
]
