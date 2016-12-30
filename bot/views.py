from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
import requests

_PAGE_TOKEN = 'EAAXmqZAwr6xoBACfVnhcUgZA09ATR9SYRU6y3i0YtZCFeIZCyxxZAgZCNZCn20eeK0lPHZBKOBXgqaAzUp1jMPzqHkdX1ZBnumZBJbz91pEfvPrpbW71EZA9BCPC46ybFehIGsaAPdL4ZCpQDKodHKAiZA0WJGxG1BZCiYXICZBPpoRbPoJbwZDZD'

def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % _PAGE_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # print(status.json())

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
                if 'message' in message:
                    # Print the message to the terminal
                    # print(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
