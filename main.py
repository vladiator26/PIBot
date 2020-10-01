from discord.ext import commands
import discord
from constants import *
import os

with open('allowed_users.txt', 'r', encoding='utf-8') as file:
    allowed_users = file.read().split('\n')

token = str(os.environ.get('token'))
bot = commands.Bot(command_prefix=prefix)
main_guild: discord.Guild
login_channel: discord.TextChannel
student_role: discord.Role


@bot.command()
async def login(context: commands.Context, *arguments):
    if context.channel != login_channel:
        pass
    if len(arguments) < 2:
        await context.channel.send("Неправильный формат")
    elif f"{arguments[0]} {arguments[1]}" not in allowed_users:
        await context.channel.send("Пользователь с таким именем отсутствует в списке группы")
    elif await check_for_duplicate(f"{arguments[0]} {arguments[1]}"):
        await context.channel.send("Пользователь с таким именем уже есть")
    else:
        await context.message.author.edit(nick=f"{arguments[0]} {arguments[1]}")
        await context.message.author.add_roles(student_role)


@bot.event
async def on_ready():
    global main_guild, login_channel, student_role
    main_guild = bot.get_guild(main_guild_id)
    login_channel = bot.get_channel(login_channel_id)
    student_role = main_guild.get_role(student_role_id)
    print("Login success")


async def check_for_duplicate(value: str):
    async for member in main_guild.fetch_members():
        if member.nick == value:
            return True
    return False


bot.run(token)
