# -*- coding: utf-8 -*-


from .. import loader, utils
import logging
import asyncio
import re

logger = logging.getLogger(__name__)

@loader.tds
class IrisBioWarMod(loader.Module):
    """Модуль для заражений в ирисе"""
    strings = {
        "name": "IrisBioWar",
        "link_id": "tg://openmessage?user_id=",
        "link_username": "https://t.me/",
        "infect": "Заразить {}",

        "successfuly_infect": "<b>Люди из списка успешно заражены</b>",
        "avenge_infection_successfuly":"<b>Все прошло успешно</b>",
        "avenge_infection_not_successfuly":"<b>Что-то пошло не так</b>",

        "laboratory_data":{
            "d": r"Досье лаборатории (.*)",
            "s": r"Руководитель: (.*)",
            "с": r"В составе Корпорации (.*)",
            "n": r"Имя патогена: (.*)",
            "q": r"Квалификация учёных: (.*)",
            "np": r"Новый патоген: (.*)",

            "inf": r"Заразность: (.*)",
            "imm": r"Иммунитет: (.*)",
            "m": r"Летальность: (.*)",
            "ss": r"Служба безопасности: (.*)",

            "be": r"Био-опыт: (.*)",
            "br": r"Био-ресурс: (.*)",

            "f": r"Руководитель в состоянии горячки(.*)"
        }
    }
    async def client_ready(self, client, db):
        db.set("Iris", "chat_biowar", 5443619563)
        db.set("Iris", "infect_later", [])

        self.client = client
        self.db = db
#----------------------------------------------------------------------------
    async def handler_link(self, link):
        if link.startswith(self.strings("link_id")):
            return "@" + link.replace(
                self.strings("link_id"), "")
        elif link.startswith(self.strings("link_username")):
            return "@" + link.replace(
                self.strings("link_username"), "")
        else:
            return False

    async def generator_links(self, entities, numbers):
        users = []
        for x in range(numbers[0]-1, numbers[1]): 
            url = await self.handler_link(entities[x][0].url) 
            if url:
                users.append(
                    url
                )
        return users

    async def generator_links_list(self, entities, numbers):
        users = []
        for x in numbers:
            url = await self.handler_link(entities[x][0].url) 
            if url:
                users.append(
                    url
                )
        return users
#----------------------------------------------------------------------------
    async def infect_listcmd(self, message):
        """Два варианта использования
        Примеры:
        .infect_list 5 2 8
        .infect_list 5-10

        Заражает людей по номерам или от и до, обязателен ответ на список"""
        reply = await message.get_reply_message()
        entities = reply.get_entities_text()
        if True if "-" in utils.get_args_raw(message) else False:
            numbers = [
                int(x) for x in utils.get_args_raw(message).split("-")
                ]   
            infected = await self.generator_links(entities, numbers)
        else:
            users_num = [
                int(x)-1 for x in utils.get_args_raw(message).split()
                ]
            infected = await self.generator_links_list(entities, users_num)
        for user in infected: 
            chat = self.db.get("Iris", "chat_biowar")
            await self.client.send_message(chat, self.strings("infect").format(user))
            await asyncio.sleep(3)
        return await utils.answer(
            message,
            self.strings("successfuly_infect")
            )
    
    async def avenge_infectioncmd(self, message):
        """Ответьте на сообщение данной командой кого хотите заразить в ответ"""
        reply = await message.get_reply_message()
        entities = reply.get_entities_text()

        if len(entities) == 4 or 3:
            chat = self.db.get("Iris", "chat_biowar")
            user = await self.handler_link(entities[1][0].url)
            await self.client.send_message(chat, self.strings("infect").format(user))
            return await utils.answer(
                message,
                self.strings("avenge_infection_successfuly")
                )
        else:
            return await utils.answer(
                message,
                self.strings("avenge_infection_not_successfuly")
                )
    
#----------------------------------------------------------------------------
    async def current_chat_biowarcmd(self, message):
        """Устанавливаеи текущий чат для заражений"""
        if message.is_private == True and message.chat_id == 707693258:
            self.db.set("Iris", "chat_biowar", 5443619563)
            return await message.edit(
                self.strings("successfuly_chat")
                )
        elif message.is_private == True:
            return await utils.answer(
                message,
                self.strings("chat_no_private")
                )
        else:
            self.db.set("Iris", "chat_biowar", message.chat_id)
            return await utils.answer(
                message,
                self.strings("successfuly_chat")
                )

    async def get_laboratorycmd(self, message):
        """Позволяет просмотреть определенные параметры своей лаборатории и всю,
        чтобы просмотреть лабораторию просто напишите команду, если хотите определенные данные
        то укажите аргументы через тире. Парамтры .get_parametrs_lab"""
        async with self.client.conversation(5443619563) as conv:
            await conv.send_message('!Лаб')
            response = await conv.get_response()
            await conv.mark_read()
        if len(utils.get_args_raw(message)) == 0:
            return await utils.answer(
                message,
                response.text
                )
        else:
            text = []
            data = self.strings("laboratory_data")
            flags = "".join(utils.get_args_raw(message).split(" ")).split("-")
            if "" in flags:
                flags.remove("")
            for flag in flags:
                search = re.search(data[flag], response.text)
                if search:
                    text.append(search.group()[:-1] if flag == "d" else search.group())
                else:
                    text.append("Параметр -{} не указан.".format(
                        flag
                    ))
            return await utils.answer(
                message,
                "\n".join(text)
                )
    async def get_parametrs_labcmd(self, message):
        """Получение параметров о лаборатории"""
        text = """
d: Имя лаборатории
s: Руководитель
с: Корпорация
n: Имя патогена
q: Квалификация учёных
np: Новый патоген через...

inf: Заразность
imm: Иммунитет
m: Летальность
ss: Служба безопасности

be: Био-опыт
br: Био-ресурс

f: Горячка руководителя"""

        return await utils.answer(
            message,
            text
            )
