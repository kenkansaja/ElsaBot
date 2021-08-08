import asyncio

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from DaisyX import telethn 
from DaisyX.events import register as cutiepii



@cutiepii(pattern="^/tagall ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Hai Teman Saya Elsa, Saya Panggil Kalian Semua"
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, 1000):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()


@cutiepii(pattern="^/users ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Users : "
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


__mod_name__ = "Tagger 🖇"
__help__ = """
  ➢ `/tagall : Tag everyone in a chat
"""
