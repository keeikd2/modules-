from .. import loader, utils  # noqa

import asyncio

import contextlib

import pytz

import re

re._MAXCACHE = 3000

import telethon

from telethon.tl.types import MessageEntityTextUrl, Message

from telethon.tl.functions.users import GetFullUserRequest

import json as JSON

from telethon.errors.rpcerrorlist import FloodWaitError

from datetime import datetime, date, time

import logging

import types

from ..inline.types import InlineCall

import random

import subprocess

import string, pickle

def validate_text(text: str):

    txt = text.replace("<u>", "").replace("</u>", "").replace("<i>", "").replace("</i>", "").replace("<b>", "").replace("</b>", "").replace("<s>", "").replace("</s>", "").replace("<tg-spoiler>", "").replace("</tg-spoiler><s>", "")

    return txt

@loader.tds

class BioMod(loader.Module):

    """

💘

    """

    strings = {
        "name": "id",

        

        "not_reply": "<emoji document_id=5215273032553078755>💔</emoji> Реплая нет.",

        

        "not_args": "<emoji document_id=5215273032553078755>💔</emoji> Аргументов нет.",

        

        "nolink": "<emoji document_id=5197248832928227386>💔</emoji> Нет ссылки.",

        "hueta": "Ничего не могу понять..💔",
              "aicmd":

            "<b>🥷🏻</b> <a href='tg://openmessage?user_id={}'>{}</a>\n"

            "<b>🆔:</b> <code>@{}</code>",

        "myid": "<b>My 🆔:</b> <code>@{}</code>",
      async def айcmd(self, message):
        
}

        """

[reply/arg]

Получает айди пользователя.

        """

        reply = await message.get_reply_message()

        args = utils.get_args(message)

        if not reply:

            

            if not args:

                user = await message.client.get_entity(message.sender_id)

                link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)

                return await message.reply(

                    f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"

                    f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"

                )

            user = 0

            if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):

                user = await message.client.get_entity(args[0])

            

            elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):

                user = args[0].replace("@", "")

                user = await message.client.get_entity(int(user))

            elif re.fullmatch(r"\d{4,14}", args[0], flags=re.ASCII):

                user = await message.client.get_entity(int(args[0]))

            

            elif re.fullmatch(r"\D\w{3,32}", args[0], flags=re.ASCII):

                user = await message.client.get_entity(args[0])

            

            if not user:

                return await message.reply("ты ввел хуйню реально")

            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)

            return await message.reply(

                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"

                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"

            )

        if not args:

            user = await message.client.get_entity(reply.sender_id)

            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)

            return await message.reply(

                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"

                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"

            )

        user = 0

        if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):

            user = await message.client.get_entity(args[0])

        

        elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):

            user = args[0].replace("@", "")

            user = await message.client.get_entity(int(user))

        elif re.fullmatch(r"\d{4,14}", args[0], flags=re.ASCII):

            user = await message.client.get_entity(int(args[0]))

        

        elif re.fullmatch(r"\D\w{3,32}", args[0], flags=re.ASCII):

            user = await message.client.get_entity(args[0])

        

        if not user:

            return await message.reply("ты ввел хуйню реально")

        link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)

        return await message.reply(

            f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"

            f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"

        )
