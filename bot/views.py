from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
import requests
from movies.models import Movie
from showtimes.models import Showtime

_PAGE_TOKEN = 'EAAXmqZAwr6xoBAKtpxW7m3tM6XrBDFFfWiQZABNZA3JzXcs7hsTspxryngttkkzeUYZCjJ2wG8DEaekZAZAIXc1kAwiLtfj2jhFYbOcuGaJRDaWyj0OqCdrxZApZCBmlUZC2p9DIAHBKJ5ghGEuUQdTFox6WvXt8cZA7cm7VDt3ZBcNJwZDZD'
post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN


def show_text_message(fbid, _data):
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": _data}})
    requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


def show_welcome_message(fbid):
    response_msg = dict()
    response_msg["recipient"] = {"id": fbid}

    payload = {
        "template_type": "button",
        "text": "What movies are you looking for?",
        "buttons": [
            {
                "type": "postback",
                "title": "Now Playing",
                "payload": "now"
            },
            {
                "type": "postback",
                "title": "Upcoming",
                "payload": "up"
            }
        ]
    }

    attachment = {
        "type": "template",
        "payload": payload,
    }

    response_msg["message"] = {"attachment": attachment}
    requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=json.dumps(response_msg))


def show_movies(fbid, movies):
    response_msg = dict()
    response_msg["recipient"] = {"id": fbid}
    elems = []

    for mv in movies:
        if mv.status == 'NP':
            action_btn = [
                {"type": "postback", "title": "Showtime", "payload": str(mv.event_id)}
            ]
        else:
            action_btn = [
                {"type": "web_url", "title": "Trailer", "url": str(mv.trailer)}
            ]
        el = {"title": str(mv.name)[0:75], "image_url": mv.poster, "subtitle": str(mv.plot)[0:75],
              "buttons": action_btn}
        elems.append(el)

    last_btn = [{"title": "View on Site", "type": "web_url", "url": "http://www.qfxcinemas.com/"}]

    payload = {
        "template_type": "list",
        "top_element_style": "compact",
        "elements": elems,
        "buttons": last_btn
    }

    attachment = {
        "type": "template",
        "payload": payload,
    }

    response_msg["message"] = {"attachment": attachment}
    requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=json.dumps(response_msg))


def show_movie_detail(fbid, _data):
    msg_dict = dict()
    msg_dict['recipient'] = {"id": fbid}

    msg_dict['message'] = dict()

    qr = []
    for d in _data:
        qr_item = dict()
        qr_item['content_type'] = "text"
        qr_item['title'] = "%s @ %s" % (str(d.time), str(d.cinema))
        qr_item['payload'] = "%s @ %s" % (str(d.time), str(d.cinema))

        qr.append(qr_item)

    msg_dict['message']['text'] = "When and Where?"
    msg_dict['message']['quick_replies'] = qr
    response_msg = json.dumps(msg_dict)
    # print response_msg
    requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '22552255':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                kw = None
                fb_id = message['sender']['id']

                print message

                if 'message' in message:
                    kw = message.get('message')['text'].lower() if 'text' in message.get('message') else None

                if 'postback' in message:
                    kw = message.get('postback')['payload'].lower() if 'payload' in message.get('postback') else None

                if kw:
                    print "this came back: %s" % str(kw)
                    self.take_action(str(kw), fb_id)

        return HttpResponse()

    def take_action(self, kw, fb_id):
        _data = 'Sorry, I cannot handle that request.'
        movies_object = Movie.objects
        showtime_object = Showtime.objects
        list_movies_id = [str(mv.event_id) for mv in movies_object.all()]
        list_showtime_id = [str(sh.id) for sh in showtime_object.all()]

        if kw == 'yo':
            show_welcome_message(fb_id)
        elif kw == 'now':
            _data = movies_object.filter(status='NP')[:4]  # only 4 entries are possible in a list template
            show_movies(fb_id, _data)
        elif kw == 'up':
            _data = movies_object.filter(status='UP')[:4]  # only 4 entries are possible in a list template
            show_movies(fb_id, _data)
        elif kw in list_movies_id:
            try:
                mv = movies_object.get(event_id=int(kw))
                _data = showtime_object.filter(movie_id=mv.id)[:11]  # quick replies can have 11 entries only
                show_movie_detail(fb_id, _data)
            except Movie.DoesNotExist:
                show_text_message(fb_id, _data)
        elif '@' in kw:
            try:
                booking_url = showtime_object.get(id=int(kw)).booking_url
                _data = "You can book your ticket here: %s" % str(booking_url)
                show_text_message(fb_id, _data)
            except Movie.DoesNotExist:
                show_text_message(fb_id, _data)
        else:
            show_text_message(fb_id, _data)
