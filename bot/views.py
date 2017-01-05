from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
import requests
from messengerbot import MessengerClient, messages, attachments, templates, elements
from movies.models import Movie
from showtimes.models import Showtime

_PAGE_TOKEN = 'EAAXmqZAwr6xoBAKtpxW7m3tM6XrBDFFfWiQZABNZA3JzXcs7hsTspxryngttkkzeUYZCjJ2wG8DEaekZAZAIXc1kAwiLtfj2jhFYbOcuGaJRDaWyj0OqCdrxZApZCBmlUZC2p9DIAHBKJ5ghGEuUQdTFox6WvXt8cZA7cm7VDt3ZBcNJwZDZD'


def post_facebook_message(fbid, _data, _type):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    msg_dict = dict()
    msg_dict['recipient'] = {"id": fbid}
    if _type == 'quick':
        msg_dict['message'] = dict()
        qr = []
        for d in _data:
            qr_item = dict()
            qr_item['content_type'] = "text"
            qr_item['title'] = "%s" % str(d.name)
            qr_item['payload'] = "%s" % str(d.name)

            qr.append(qr_item)

        msg_dict['message']['text'] = "Pick a movie:"
        msg_dict['message']['quick_replies'] = qr
        response_msg = json.dumps(msg_dict)
    else:
        response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": _data}})

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


def show_text_message(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": _data}})

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


def show_mov_temp(fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    response_msg = dict()

    response_msg["recipient"] = {"id": fbid}

    btns = [{"title": "Book Now", "type": "web_url", "url": "http://niteshrijal.com.np", "messenger_extensions": True,
             "webview_height_ratio": "tall", "fallback_url": "http://niteshrijal.com.np"}]

    defac = {"type": "web_url", "url": "http://niteshrijal.com.np", "messenger_extensions": True,
             "webview_height_ratio": "tall", "fallback_url": "http://niteshrijal.com.np"
             }

    elems = [{"title": "Classic White T-Shirt",
              "image_url": "https://peterssendreceiveapp.ngrok.io/img/white-t-shirt.png",
              "subtitle": "10 Cotton, 20 Comfortable",
              "default_action": defac,
              "buttons": btns
              }]

    last_btn = [{"title": "View More", "type": "postback", "payload": "now"}]

    paylo = {
        "template_type": "list",
        "top_element_style": "compact",
        "elements": elems,
        "buttons": last_btn
    }

    attc = {
        "type": "template",
        "payload": paylo,
    }

    response_msg["message"] = {"attachment": attc}

    mm = json.dumps(response_msg)
    print(mm)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=mm)


def show_movie_list(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    msg_dict = dict()
    msg_dict['recipient'] = {"id": fbid}

    msg_dict['message'] = dict()
    qr = []
    for d in _data:
        qr_item = dict()
        qr_item['content_type'] = "text"
        qr_item['title'] = "%s" % str(d.name)
        qr_item['payload'] = "%s" % str(d.name)

        qr.append(qr_item)

    msg_dict['message']['text'] = "What Movie?"
    msg_dict['message']['quick_replies'] = qr
    response_msg = json.dumps(msg_dict)

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


def show_welcome_message(messenger, recipient):
    btn_now_playing = elements.PostbackButton(
        title='Now Playing',
        payload='now'
    )

    btn_up_coming = elements.PostbackButton(
        title='Upcoming',
        payload='up'
    )

    template_btn = templates.ButtonTemplate(
        text='What movies are you looking for?',
        buttons=[btn_now_playing, btn_up_coming]
    )

    attachment = attachments.TemplateAttachment(template=template_btn)

    message = messages.Message(attachment=attachment)
    request = messages.MessageRequest(recipient, message)
    messenger.send(request)


def show_movies(messenger, recipient, _data):
    btns = []

    for d in _data:
        btn = elements.PostbackButton(
            title=str(d.name),
            payload=str(d.name)
        )

        btns.append(btn)

    template_btn = templates.ButtonTemplate(
        text='Which Movie?',
        buttons=btns
    )

    attachment = attachments.TemplateAttachment(template=template_btn)

    message = messages.Message(attachment=attachment)
    request = messages.MessageRequest(recipient, message)
    messenger.send(request)


def show_movie_detail(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
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

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


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
        movies_object = Movie.objects
        showtime_object = Showtime.objects
        list_movies = [str(mv.name).lower() for mv in movies_object.all()]
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    fb_id = message['sender']['id']
                    messenger = MessengerClient(access_token=_PAGE_TOKEN)
                    recipient = messages.Recipient(recipient_id=fb_id)
                    _data = 'Sorry, I cannot handle that request.'
                    kw = message.get('message')['text'].lower() if 'text' in message.get('message') else None
                    print "here: %s" % str(kw)
                    if kw == 'yo':
                        show_mov_temp(fb_id)
                        # show_welcome_message(messenger, recipient)
                    # elif kw == 'now':
                    #     _data = movies_object.filter(status='NP')
                    #     show_movies(messenger, recipient, _data)
                    # elif kw == 'up':
                    #     _data = movies_object.filter(status='UP')
                    #     show_movies(messenger, recipient, _data)
                    # elif kw in list_movies:
                    #     try:
                    #         mv = movies_object.get(name__iexact=kw)
                    #         _data = showtime_object.filter(movie_id=mv.id)
                    #         show_movie_detail(fb_id, _data)
                    #     except Movie.DoesNotExist:
                    #         show_text_message(fb_id, _data)
                    else:
                        show_text_message(fb_id, _data)
        return HttpResponse()
