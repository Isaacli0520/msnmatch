from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import User
from django.db.models import Q
from channels.db import database_sync_to_async
import asyncio
import json
import os


class FilterConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.event = asyncio.Event()
        # self.from_user_name = self.scope['url_route']['kwargs']['from_user_name']
        self.user = self.scope["user"]
        self.group_name = "filter_group"

        # await self.channel_layer.group_add(
        #     self.group_name,
        #     self.channel_name,
        # )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        # print("data received", text_data_json)
        if command == 'join':
            self.group_name = "filter-" + str(text_data_json['slide_pk'])
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'type':'join',
                'slide_pk':text_data_json['slide_pk'],
            }))
        elif command == 'send':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':"comment_unfiltered",
                    'text': text_data_json['text'],
                    'color': text_data_json['color'],
                    'size': text_data_json['size'],
                    'time': text_data_json['time'],
                    'mode': text_data_json['mode'],
                    'message_type':text_data_json['message_type'],
                }
            )

    async def comment_unfiltered(self, text_data):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':"comment_unfiltered",
            'text': text_data['text'],
            'color': text_data['color'],
            'size': text_data['size'],
            'time': text_data['time'],
            'mode': text_data['mode'],
            'message_type':text_data['message_type'],
        }))

class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.event = asyncio.Event()
        # self.from_user_name = self.scope['url_route']['kwargs']['from_user_name']
        self.user = self.scope["user"]
        self.group_name = "comments_group"

        # await self.channel_layer.group_add(
        #     self.group_name,
        #     self.channel_name,
        # )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        if command == 'join':
            self.group_name = "comments-" + str(text_data_json['slide_pk'])
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'type':'join',
                'slide_pk':text_data_json['slide_pk'],
            }))
        elif command == 'send':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':"comment_filtered",
                    'text': text_data_json['text'],
                    'color': text_data_json['color'],
                    'size': text_data_json['size'],
                    'time': text_data_json['time'],
                    'question_id':text_data_json['question_id'],
                    'mode': text_data_json['mode'],
                    'message_type':text_data_json['message_type'],
                }
            )
        elif command == 'question_page':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':"question_command",
                    'direction':text_data_json['direction'],
                }
            )

    async def question_command(self, text_data):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':"question_command",
            'direction':text_data['direction'],
        }))

    async def comment_filtered(self, text_data):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':"comment_filtered",
            'text': text_data['text'],
            'color': text_data['color'],
            'size': text_data['size'],
            'time': text_data['time'],
            'question_id':text_data['question_id'],
            'mode': text_data['mode'],
            'message_type':text_data['message_type'],
        }))
