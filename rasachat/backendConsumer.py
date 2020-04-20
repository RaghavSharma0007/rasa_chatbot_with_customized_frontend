from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.utils import EndpointConfig
interpreter = NaturalLanguageInterpreter.create('rasachat/models/current/nlu')
endpoint = EndpointConfig('http://localhost:5055/webhook')
agent = Agent.load('rasachat/models/dialogue', interpreter=interpreter, action_endpoint=endpoint)
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']

       
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #print("received",message)
        responses = agent.handle_text(message, sender_id=self.room_group_name)
        #print(responses)
        # if responses.__len__()>0:
        #     print("response is not empty===")
        #     for r in responses:
        #         print(r)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': responses,
                'msg_type':""
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        #print("Send message to WebSocket")
        await self.send(text_data=json.dumps({
            'message': message,
            'type':'bot_uttered',
            'msg_type':""
        }))
