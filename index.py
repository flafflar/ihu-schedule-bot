import os
import discord

import bot

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as %s" % self.user)

    async def on_message(self, message):
        if message.author == self.user: return
        answer = bot.answer(message.content)
        if answer:
            await message.channel.send(answer)

client = MyClient()
client.run(os.getenv('DISCORD_TOKEN'))
