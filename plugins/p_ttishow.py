import time, asyncio, os, sys
import pytz
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, MELCOWE_IMG, CHNL_LNK, GRP_LNK
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired
import asyncio

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('🤖 sᴜᴘᴘᴏʀᴛ 🤖', url=f'https://t.me/{SUPPORT_CHAT}')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>𝗖𝗛𝗔𝗧 𝗡𝗢𝗧 𝗔𝗟𝗟𝗢𝗪𝗘𝗗\n\nMʏ ᴀᴅᴍɪɴꜱ ʜᴀꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴍᴇ ғʀᴏᴍ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ ! Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɪᴛ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('🔰 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 🔰', url=CHNL_LNK)
        ],[
            InlineKeyboardButton('❗ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ❗', url=GRP_LNK)
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>ᴛʜᴀɴᴋʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title} 🥀\n\nɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇꜱᴛɪᴏɴꜱ & ᴅᴏᴜʙᴛꜱ ᴀʙᴏᴜᴛ ᴜꜱɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ</b>",
            reply_markup=reply_markup)
    else:
        for user in message.new_chat_members:
            try:
                image = await bot.download_media(user.photo.big_file_id)
            except:
                image = MELCOWE_IMG
    timez = "Asia/Kolkata"
    mr = datetime.now(pytz.timezone(f'{timez}'))
    date = mr.strftime('%d/%m/%y')
    time = mr.strftime('%I:%M:%S %p')
    chat_member_p = await message.chat.get_member(message.from_user.id)
    joined_date = (chat_member_p.joined_date or datetime.now(pytz.timezone(f'{timez}'))).strftime("%d/%m/%Y")
    joined_time = (datetime.now(pytz.timezone(f'{timez}'))).strftime("%I:%M:%S")
    joined_day = (chat_member_p.joined_date or datetime.now(pytz.timezone(f'{timez}'))).strftime("%A")
    text = f'''
<b>🦋 ʜᴇʏ ʙᴜᴅᴅʏ {user.mention}\n\n✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {(await bot.get_chat(message.chat.id)).title} ❤️</b>

<b>┌ ꜰɪʀsᴛ ɴᴀᴍᴇ :</b> {user.first_name}
<b>├ ɪᴅ :</b> <code>{user.id}</code>
<b>├ ʟᴀsᴛ ɴᴀᴍᴇ :</b> {user.last_name or '~'}
<b>├ ᴜsᴇʀ ɴᴀᴍᴇ :</b> {'@' + user.username if user.username else '~'}
<b>├ ʟᴀɴɢᴜᴀɢᴇ :</b> {user.language_code.upper() if user.language_code else '~'}
<b>├ ᴅᴄ ɪᴅ :</b> {user.dc_id or '~'}
<b>└ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ :</b> {'ʏᴇs' if user.is_premium else 'ɴᴏ'}

<b>┌ ᴊᴏɪɴᴇᴅ ᴛɪᴍᴇ :</b> <code>{joined_time}</code>
<b>├ ᴊᴏɪɴᴇᴅ ᴅᴀʏ :</b> <code>{joined_day}</code>
<b>└ ᴊᴏɪɴᴇᴅ ᴅᴀᴛᴇ :</b> <code>{joined_date}</code>'''
    buttons = [[
        InlineKeyboardButton('🔰 ɢʀᴏᴜᴘ ʀᴜʟᴇs​ 🔰', url='https://graph.org/%F0%9D%97%9A%F0%9D%97%A5%F0%9D%97%A2%F0%9D%97%A8%F0%9D%97%A3-%F0%9D%97%A5%F0%9D%97%A8%F0%9D%97%9F%F0%9D%97%98%F0%9D%97%A6-10-29')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await message.reply_photo(
        photo=image,
        reply_markup=reply_markup,
        caption=text,
        parse_mode=enums.ParseMode.HTML,
        disable_notification=True
    )
    await asyncio.sleep(50)
    await m.delete()
