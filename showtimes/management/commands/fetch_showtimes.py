from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import datetime
from movies.models import Movie
from showtimes.models import Showtime

class Command(BaseCommand):
    help = 'scrap the showtimes from qfx site, store in db locally'

    def handle(self, *args, **options):
        _base_url = 'http://www.qfxcinemas.com/'
        _booking_uri = '/Home/GetShowTimeAndTheatreByEventId?EventId=%d&oldIndex=%d&index=%d'

        movies = Movie.recent.filter(status='NP')
        for mv in movies:
            mv.movies.all().delete()
            self.stdout.write(self.style.SUCCESS("Fetching Showtimes for %s" % mv.name))
            _booking_urls = [
                                urljoin(_base_url, _booking_uri % (mv.event_id, 0, 0)),
                                urljoin(_base_url, _booking_uri % (mv.event_id, 0, 1)),
                                urljoin(_base_url, _booking_uri % (mv.event_id, 1, 2))
                            ]
            i = 0
            for _booking_url in _booking_urls:
                result = requests.get(_booking_url)
                if result.status_code == 200:
                    soup = BeautifulSoup(result.content, 'html.parser')
                    for shows in soup.find_all("div", "show-movies"):
                        show_hall_name = shows.find("h2", "show-hall-name").text
                        show_times = shows.find_all("a")

                        if not Showtime.get_cinemahall_code(show_hall_name):
                            continue

                        for st in show_times:
                            time = st.text.strip()
                            _url = st.get('href')

                            booking_url = urljoin(_base_url, _url)
                            showtime = Showtime.objects.create(date=datetime.datetime.utcnow()+datetime.timedelta(days=i), movie=mv, cinema=Showtime.get_cinemahall_code(show_hall_name), time=time, booking_url=booking_url)
                    i += 1
                elif result.status_code == 500:
                    pass
                else:
                    self.stdout.write(self.style.ERROR("HTTP: %d" % int(result.status_code)))
