import os
import discord
import random

from discord.ext import commands
from ballreplies import replies
from purgereplies import preplies

client = commands.Bot(command_prefix='>')

# we dont talk about what is above

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
      await ctx.send(f'Question: ```CSS\n{question}```\nAnswer: ```CSS\n{random.choice(replies)}```')


@client.command(aliases = ['purge'])
async def clear(ctx, amount = 5 + 1): 
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.manage_messages:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send(f"{random.choice(preplies)}")


@client.command()
async def ping(ctx):
    """shows the latency between the client and the server in miliseconds"""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.event
async def on_member_join(member):
    """logs a message when a user joins the server"""
    print(f"{member} has joined the server!")


@client.event
async def on_member_remove(member):
    """logs a message when a user leaves the server"""
    print(f"{member} has left the server.")



client.run(os.environ.get("DISCORD_BOT_SECRET"))
