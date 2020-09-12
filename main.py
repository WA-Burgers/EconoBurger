import os
import discord
import random

from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix='>')

# we dont talk about what is above

# adding another comment?


@client.event
async def on_ready():
    """runs when bot comes online"""
    print(f"Init as {client.user}")


@client.event
async def on_message(message):
    """an event that happens when any message is sent"""
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )
    if message.author == client.user:
        return

    if "hello" in message.content.lower():
        await message.channel.send('Hi!')

    await client.process_commands(message)

    
@client.command(aliases=['8ball',]) #8ball WOOOOOOO!
async def _8ball(ctx, *, question):
      responses = ["It is certain.",
                  "It is decidedly so.",
                  "Without a doubt.",
                  "Yes - definitely.",
                  "You may rely on it.",
                  "As I see it, yes.",
                  "Most likely.",
                  "Outlook good.",
                  "Yes.",
                  "Signs point to yes.",
                  "Reply hazy, try again.",
                  "Ask again later.",
                  "Better not tell you now.",
                  "Cannot predict now.",
                  "Concentrate and ask again.",
                  "Don't count on it.",
                  "My reply is no.",
                  "Ask Hybrid about it",
                  "Ask NullCube about it",
                  "My sources say no.",
                  "Outlook not so good.",
                  "Very doubtful."]
      await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def ping(ctx):
    """shows the latency between the client and the server in miliseconds"""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.event
async def on_member_join(member):
    """logs a message when a user joins the server"""
    print(f'{member} has joined the server!')


@client.event
async def on_member_remove(member):
    """logs a message when a user leaves the server"""
    print(f'{member} has left the server.')


keep_alive()  # keeps the repl running
client.run(os.environ.get("DISCORD_BOT_SECRET"))
