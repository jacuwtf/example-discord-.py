import discord
import random
import asyncio
import logging
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')
TOKEN = open("TOKEN.TXT", "r").read()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('.help'))
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')

#ping

@bot.command()
async def ping(ctx):
  embed = discord.Embed(title="Ping", color=0x0c0f27)
  embed.add_field(name="Bot", value=f'🏓 Pong! {round(bot.latency * 1000)}ms')
  embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

#ping

#help

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot", description="Commands:", color=0x0c0f27)
    embed.add_field(
        name=".help", value="Gives this message.", inline=False)
    embed.add_field(
        name=".ping", value="Pings the bot.", inline=False)
    embed.add_field(
        name=".kick", value="Kicks a member.", inline=False)
    embed.add_field(
        name=".ban", value="Bans a member.", inline=False)
    embed.add_field(
        name=".clear", value="Clears the `x` amount of messages specified.", inline=False)

    await ctx.send(embed=embed)

#help

#clear


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    deletemessage = await ctx.send(f"{amount} messages got deleted.")
    await asyncio.sleep(3)
    await deletemessage.delete()

#clear

#kick


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}\nReason: {reason}')

#kick

#ban


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}\nReason: {reason}')

#ban

#unban


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#unban

#background tasks

@bot.event
async def on_command_error(ctx, error):
    logging.error(f'Error on command {ctx.invoked_with}, {error}')
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error!",
                              description=f"The command `{ctx.invoked_with}` was not found! We suggest you do `.help` to see all of the commands",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        embed = discord.Embed(title="Error!",
                              description=f"You don't have permission to execute `{ctx.invoked_with}`.",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error!",
                              description=f"`{error}`",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
        raise error

#background tasks

bot.run(TOKEN)
