from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
from movies.models import Movie

class Command(BaseCommand):
    help = 'scrap the movies from qfx site, store in db locally'

    def handle(self, *args, **options):
        _base_url = 'http://www.qfxcinemas.com/'
        _np_detail_url = '/Home/GetMovieDetails?EventID=%d'
        _np_ticket_url = '/Home/GetTicketBookDetail?EventID=%d'
        _thumb_url = '/Home/GetThumbnailImage?EventID=%d'
        _trailer_url = 'https://www.youtube.com/watch?v=%s'
        result = requests.get(_base_url)
        if result.status_code == 200:
            self.stdout.write(self.style.SUCCESS("URL: %s" % _base_url))
            soup = BeautifulSoup(result.content, 'html.parser')
            movies_block = soup.find("div", "content")
            category_block = movies_block.find_all("div", "movies")
            now_playing = category_block[0]
            up_coming = category_block[1]

            # fetch now_playing movies
            for movie in now_playing.find_all("div", "movie"):
                name = str(movie.find("h4", "movie-title").text)
                event_id = int(movie.find("a").get('href').split('=')[-1])
                image = urljoin(_base_url, _thumb_url % event_id)
                status = 'NP'
                mv = Movie.objects.create(name=name, event_id=event_id, image=image)

                # fetch other details like runtime, trailer and plot from details url
                _det_url = urljoin(_base_url, _np_detail_url % event_id)
                details = requests.get(_det_url)
                if details.status_code == 200:
                    self.stdout.write(self.style.SUCCESS("URL: %s" % _det_url))
                    dsoup = BeautifulSoup(details.content, 'html.parser')
                    # import ipdb; ipdb.set_trace()
                    video_id = str(dsoup.find("input", type="hidden").get('value'))
                    plot = str(dsoup.find_all("div", "mar-t-15")[-1].find("p").text)

                    print video_id, plot
                    # break
                    # TODO: get runtime here

                    # save these extra fields
                    mv.trailer = _trailer_url % video_id
                    mv.plot = plot
                    # TODO: save runtime here
                    mv.save()
                else:
                    self.stdout.write(self.style.ERROR("DETAILS NOT FOUND"))

        else:
            self.stdout.write(self.style.ERROR("HTTP: %d" % int(result.status_code)))
