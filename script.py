import discord
from discord.ext import commands
import re
import os
import asyncio
import argparse
from googletrans import Translator
import random

bot = commands.Bot(command_prefix='lb.')

opted_out = False
users_opted_out = []

languages = ["af", "sq", "ar", "be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
             "vi", "cy", "yi"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.content == "lb.optout":
        if message.author.id in users_opted_out:
            await bot.send_message(message.channel, ":x: You are already opted out of LinguaBot.")
        else:
            users_opted_out.append(message.author.id)
            await bot.send_message(message.channel, ":white_check_mark: You are now opted out of LinguaBot.")
    elif message.content == "lb.optin":
        if message.author.id not in users_opted_out:
            await bot.send_message(message.channel, ":x: You are already opted into LinguaBot.")
        else:
            users_opted_out.remove(message.author.id)
            await bot.send_message(message.channel, ":white_check_mark: You are now opted into LinguaBot.")
    elif message.author.id in users_opted_out or message.author == bot.user:
        return
    else:
        bot.loop.create_task(background_translate(message.channel, message.content, message.author.id))

async def background_translate(channel, text, userid):
    await bot.wait_until_ready()
    translator = Translator()
    translation = text
    translation = translator.translate(translation, dest=languages[int(userid) % 52]).text
    await bot.send_message(channel, translation)

bot.run('token')
