from django.shortcuts import render, redirect
from django.http import Http404
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
import json
from asgiref.sync import async_to_sync


def index(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        option = request.POST.get("option")
        return redirect('/play/%s?&option=%s' %(room_id, option)
        )
    return render(request, "index.html", {})

def game(request, room_id):
    option = request.GET.get("option")
    if option not in ['X', 'O']:
        raise Http404("Incorrect Choice")
    context = {
        "option": option, 
        "room_id": room_id
    }
    return render(request, "tictac.html", context)


# class TicTacAPI(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = 'room_%s' % self.room_name
        
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         print("Left the room successfully")

#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
    
#     async def receive(self, text_data):
#         """Receiving messages from WebSocket. Get the events and send them accordingly. """
#         response = json.loads(text_data)
#         event = response.get("event", None)
#         message = response.get("message", None)

#         if event == 'MOVE':
#             await self.channel_layer.group_send(self.room_group_name, {
#                 'type': 'send_message',
#                 'message': message,
#                 "event": "MOVE"
#             })
            
#         if event == 'START':
#             await self.channel_layer.group_send(self.room_group_name, {
#                 'type': 'send_message',
#                 'message': message,
#                 'event': "START"
#             })
            
#         if event == 'END':
#             await self.channel_layer.group_send(self.room_group_name, {
#                 'type': 'send_message',
#                 'message': message,
#                 'event': "END"
#             })

#     async def send_message(self, request):
#         await self.send(text_data=json.dumps({
#             "payload": request,
#         }))



class TicTacAPI(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Left the room successfully")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        """Receiving messages from WebSocket. Get the events and send them accordingly. """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)

        if event == 'MOVE':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'send_message',
                    'message': message,
                    "event": "MOVE"
                }
            )
            
        if event == 'START':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'send_message',
                    'message': message,
                    'event': "START"
                }
            )
            
        if event == 'END':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'send_message',
                    'message': message,
                    'event': "END"
                }
            )

    def send_message(self, request):
        self.send(text_data=json.dumps(
                {
                    "payload": request,
                }
            )
        )
