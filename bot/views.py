from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
import requests
from movies.models import Movie
from showtimes.models import Showtime

_PAGE_TOKEN = 'EAAXmqZAwr6xoBAKtpxW7m3tM6XrBDFFfWiQZABNZA3JzXcs7hsTspxryngttkkzeUYZCjJ2wG8DEaekZAZAIXc1kAwiLtfj2jhFYbOcuGaJRDaWyj0OqCdrxZApZCBmlUZC2p9DIAHBKJ5ghGEuUQdTFox6WvXt8cZA7cm7VDt3ZBcNJwZDZD'

def post_facebook_message(fbid, _data, _type):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    msg_dict = dict()
    msg_dict['recipient'] = {"id":fbid}
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
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":_data}})

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def show_text_message(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":_data}})

    print(response_msg)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def show_movie_list(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    msg_dict = dict()
    msg_dict['recipient'] = {"id":fbid}

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

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def show_movie_detail(fbid, _data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    msg_dict = dict()
    msg_dict['recipient'] = {"id":fbid}

    msg_dict['message'] = dict()

  #   sss = json.dumps({
  # "recipient":{
  #   "id":fbid
  # }, "message":{
  #   "attachment":{
  #     "type":"template",
  #     "payload":{
  #       "template_type":"generic",
  #       "elements": [{
  #           "title": "Yo...",
  #           "image_url":"https://petersfancybrownhats.com/company_image.png",
  #           "subtitle":"Wve got the right hat for everyone.",
  #           "buttons":[
  #             {
  #               "type":"web_url",
  #               "url":"aa",
  #               "title":"Watch Trailer"
  #             },
  #             {
  #               "type":"web_url",
  #               "url":"bb",
  #               "title":"Watch Trailer"
  #             },
  #           ]
  #       }],
  #     }
  #   }
  # }

# })

    # print sss

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

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

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
        _type = 'quick'
        _data = 'Sorry, I cannot handle the request.'
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    fb_id = message['sender']['id']
                    # Print the message to the terminal
                    kw = message.get('message')['text'].lower() if 'text' in message.get('message') else None
                    if kw == 'now':
                        _data = movies_object.filter(status='NP')
                        show_movie_list(message['sender']['id'], _data)
                    elif kw in list_movies:
                        try:
                            mv = movies_object.get(name__iexact=kw)
                            _data = showtime_object.filter(movie_id=mv.id)
                            show_movie_detail(fb_id, _data)
                        except Movie.DoesNotExist:
                            show_text_message(fb_id, _data)
                    elif kw == 'test':
                        from pymessenger.bot import Bot
                        from pymessenger import Element
                        bot = Bot(_PAGE_TOKEN)
                        elements = []
                        element = Element(title="test", image_url="", subtitle="subtitle", item_url="http://arsenal.com")
                        elements.append(element)
                        bot.send_generic_message(fb_id, elements)
                    elif kw == 'mmm':
                        from message import SendMessage
                        message = SendMessage(fb_id)
                        project_styletrip = GenericElement('Chinese 111',
                                                           'do not say',
                                                           'styletrip/introduction.jpeg', [
                                                               ActionButton(ButtonType.POSTBACK,
                                                                            'test',
                                                                            payload=Payload.INTRODUCE.name)
                                                           ])
                        project_movie_lol = GenericElement('Movie lol App',
                                                           'some pp',
                                                           'movielol/introduction.jpeg', [
                                                               ActionButton(ButtonType.WEB_URL,
                                                                            'GitHub',
                                                                            url='https://github.com/enginebai/Movie-lol-android')
                                                           ])
                        message.build_generic_message([project_styletrip, project_movie_lol]).send_message()
                    elif kw == 'zzz':
                        from messengerbot import MessengerClient, messages, attachments, templates, elements
                        messenger = MessengerClient(access_token=_PAGE_TOKEN)
                        recipient = messages.Recipient(recipient_id=fb_id)
                        # Send button template
                        web_button = elements.WebUrlButton(
                           title='Show website',
                           url='https://petersapparel.parseapp.com'
                        )
                        postback_button = elements.PostbackButton(
                           title='Start chatting',
                           payload='USER_DEFINED_PAYLOAD'
                        )
                        template = templates.ButtonTemplate(
                           text='What do you want to do next?',
                           buttons=[
                               web_button, postback_button
                           ]
                        )
                        attachment = attachments.TemplateAttachment(template=template)

message = messages.Message(attachment=attachment)
request = messages.MessageRequest(recipient, message)
messenger.send(request)
                    else:
                        show_text_message(fb_id, _data)

                    # post_facebook_message(message['sender']['id'], _data, _type)
        return HttpResponse()
