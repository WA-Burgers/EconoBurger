import os
import discord
import random
import json

from discord.ext import commands, tasks
from ballreplies import replies
from workreplies import wreplies
from itertools import cycle
from permissiondeniedreplies import preplies

client = commands.Bot(command_prefix='$')
status = cycle(['Watching being worked on', 'Watching me causing the programmers pain'])

# we dont talk about what is above

@client.event
async def on_ready():
    change_status.start()
    print(f"Init as {client.user}")

@tasks.loop(minutes=20)
async def change_status(): 
    await client.change_presence(activity=discord.Game(next(status)))
    

@client.command(aliases = ['bal',])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"] 
    bank_amt = users[str(user.id)]["bank"] 

    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = "Wallet balance", value = wallet_amt)
    em.add_field(name = "Bank balance", value = bank_amt)
    await ctx.send(embed = em)

@client.command()
async def work(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(300)

    embed = discord.Embed()
    embed.color = discord.Color.green()
    embed.title = f"{random.choice(wreplies)}\nYou got the amount ¥{earnings}"
    await ctx.send(embed=embed)

    users[str(user.id)]["wallet"] += earnings

    with open ("mainbank.json", "w") as f:
        json.dump(users,f)

#used to deposit money from your wallet into your account
@client.command()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please enter the amount."
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "You don't have that much money in your wallet!"
        await ctx.send(embed=embed)
        return
    if amount<0:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please input a positive number!"
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")

    embed = discord.Embed()
    embed.color = discord.Color.green
    embed.title = f"You deposited {amount} into your account!"
    await ctx.send(embed=embed) 

#used to send a user money from your account
@client.command()
async def send(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please enter the amount."
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "You don't have that much money in your account!"
        await ctx.send(embed=embed)
        return
    if amount<0:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please input a positive number!"
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(member,amount, "bank")

    embed = discord.Embed()
    embed.color = discord.Color.green
    embed.title = f"You gave {amount} from your account!"
    await ctx.send(embed=embed)

#used to take money out of your account and put into your wallet
@client.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please enter the amount."
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "You don't have that much money in your account!"
        await ctx.send(embed=embed)
        return
    if amount<0:
        embed = discord.Embed()
        embed.color = discord.Color.red
        embed.title = "Transaction failed"
        embed.description = "Please input a positive number!"
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount, "bank")

    embed = discord.Embed()
    embed.color = discord.Color.green
    embed.title = f"You withdrew {amount} from your account!"
    await ctx.send(embed=embed)    

async def open_account(user):

    users = await get_bank_data()

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open ("mainbank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users 

async def update_bank(user,change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open ("mainbank.json", "w") as f:
        json.dump(users,f)
    return True
    
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return user

@client.command(aliases=['8ball',]) #8ball WOOOOOOO!
async def _8ball(ctx, *, question):
    embed = discord.Embed()
    embed.color = discord.Color.green()
    embed.title = "Magic 8 Ball"
    embed.description = f'Question: {question}\nAnswer: {random.choice(replies)}'
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'`Invalid command used`')

@client.command(aliases = ['purge'])
async def clear(ctx, amount : int): 
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.manage_messages:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send(f"`{random.choice(preplies)}`")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`Please specify an amount of messages to delete.`')


@client.command()
async def ping(ctx):
    """shows the latency between the client and the server in miliseconds"""
    await ctx.send(f'`Pong! {round(client.latency * 1000)}ms`')


@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'`Kicked {member.mention}`')
    else:
        await ctx.send(f"`{random.choice(preplies)}`")


@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'`Banned {member.mention}`')
    else:
        await ctx.send(f"`{random.choice(preplies)}`")


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
                await ctx.send(f'`Unbanned {user.mention}`')
                return
    else:
        await ctx.send(f"`{random.choice(preplies)}`")


@client.event
async def on_member_join(member):
    """logs a message when a user joins the server"""
    await ctx.send(f"`{member} has joined the server!`")


@client.event
async def on_member_remove(member):
    """logs a message when a user leaves the server"""
    await ctx.send(f"`{member} has left the server.`")



client.run(os.environ.get("DISCORD_BOT_SECRET"))