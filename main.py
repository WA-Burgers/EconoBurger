import os
import discord
import random

from discord.ext import commands, tasks
from ballreplies import replies
from itertools import cycle
from permissiondeniedreplies import preplies

client = commands.Bot(command_prefix='>')
status = cycle(['Watching being worked on', 'Watching me causing the programmers pain'])

# we dont talk about what is above

@client.event
async def on_ready():
    change_status.start()
    print(f"Init as {client.user}")

@tasks.loop(minutes=20)
async def change_status(): 
    await client.change_presence(activity=discord.Game(next(status)))
    
@client.command(aliases=['8ball',]) #8ball WOOOOOOO!
async def _8ball(ctx, *, question):
    embed = discord.Embed()
    embed.color = discord.Color.purple()
    embed.title = f"Magic 8 Ball"
    embed.description = f'Question: {question}\n\nAnswer: {random.choice(replies)}'
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'Invalid command used'
        embed.description = "Please check your syntax and try again :D"
        await ctx.send(embed=embed)

@client.command(aliases = ['purge'])
async def clear(ctx, amount : int): 
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.manage_messages:
        await ctx.channel.purge(limit=amount)
    else:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'{random.choice(preplies)}'
        await ctx.send(embed=embed)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'error'
        embed.description = f'Please specify the number of messages to delete :D'
        await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    """shows the latency between the client and the server in miliseconds"""
    await ctx.send(f'`Pong! {round(client.latency * 1000)}ms`')


@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed()
        embed.color = discord.Color.orange()
        embed.title = f'Kicked {member.mention}'
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'{random.choice(preplies)}'
        await ctx.send(embed=embed)


@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.ban_members:
        await member.ban(reason=reason)
        embed = discord.Embed()
        embed.color = discord.Color.orange()
        embed.title = f'Banned {member.mention}'
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'{random.choice(preplies)}'
        await ctx.send(embed=embed)


@client.command()
async def unban(ctx, *, member):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.ban_members:
        banned_users = await ctx.guild.bans()
        member_name , member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed()
                embed.color = discord.Color.orange()
                embed.title = f'Unbanned {member.mention}'
                await ctx.send(embed=embed)
                return
    else:
        embed = discord.Embed()
        embed.color = discord.Color.red()
        embed.title = f'{random.choice(preplies)}'
        await ctx.send(embed=embed)


# @client.event
# async def on_member_join(member):
#     """logs a message when a user joins the server"""
#     await ctx.send(f"`{member} has joined the server!`")


# @client.event
# async def on_member_remove(member):
#     """logs a message when a user leaves the server"""
#     await ctx.send(f"`{member} has left the server.`")



client.run(os.environ.get("DISCORD_BOT_SECRET"))