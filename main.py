
import discord

token = open("token.text", "r").read()

client = discord.Client()

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):  # event that happens per any message.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if str(message.author) == "Hybrid21#2182" and "hello" in message.content.lower():
        await message.channel.send('Hi!')

client.run(token)

