import discord
from discord.ext.commands import Bot
from discord.ext import commands
from pprint import pprint
import sys
import json
import asyncio
import random
import time
import requests
#from pokedex import pokedex
#from google import search

# мой id = 252824719764619264
# welcome chat id = 526081686027632691
TOKEN = "NTI1OTkwMTAwMzc1NTY4Mzk1.DwgJcw.q5EgzYBKhZjGOtX5Btsmb4oe5uk"

bot = commands.Bot(command_prefix="=")
bot.remove_command('help')


# Запуск бота
@bot.event
async def on_ready():
    print('Logged in as')
    print(str("User name: ") + bot.user.name)
    print('------')
    print('bot id:')
    print(bot.user.id)
    print('------')
    print(str("Discord API ver: ") + discord.__version__)
    ###
    #game = discord.Game("=help | Discord API")  # Выбор активности в статусе
    #await bot.change_presence(status=discord.Status.online, activity=game, afk=False)  # Status
    ###
    print(" ")
    print('Old man is online and ready to use ;)')

#Ошибки
@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Вы забыли указать параметр. Прочитайте указание по применению по команде **=help**")
        #await asyncio.sleep(5)
        #await channel.purge(limit=1)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Такой команды не cуществует (пока что😃)")
        #await asyncio.sleep(3)
        #await channel.purge(limit=1)

# Повторение слов
@bot.command()
async def say(ctx, *, words):
    channel = ctx.message.channel

    await channel.purge(limit=1)
    await ctx.send(words)

# Приветствие в две стороны
@bot.command()
async def greet(ctx, member: discord.Member = None):
    if ctx.message.author.id == 252824719764619264:
        # await ctx.send("Ежжи как жизнь " + member.mention + " <:kama:336765358448967683>")
        await ctx.send(f"Ежжи как жизнь, {member} <:kama:336765358448967683>")
    else:
        # await ctx.send(ctx.author.mention + " Саси бибу лох")
        await ctx.send(f"Саси бибу, {ctx.author}")

# Роль для новоприбывших
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    roleNelocal = discord.utils.get(member.guild.roles, name="Нелокальные")
    await member.add_roles(roleNelocal)
    await channel.send("Бобро поржаловать " + member.mention)
    await asyncio.sleep(1)
    await channel.send("Введите кодовое слово для получения особой роли. Если в не знаете таких слов - проигнорируйте это сообщение.")

# Обозначение роли по сообщению
@bot.event
async def on_message(message):
    channel = bot.get_channel(528246174956650506)
    roleKozak = discord.utils.get(message.guild.roles, name="Козакесы")
    roleLocal = discord.utils.get(message.guild.roles, name="Локальные")
    roleNelocal = discord.utils.get(message.guild.roles, name="Нелокальные")
    rolenames = [role.name for role in message.author.roles]
    if message.channel.id == channel.id:
        if "Козакесы" in rolenames:
            await message.channel.send("У тебя уже есть роль Козакесы")
            await channel.purge(limit=100)
        else:
            if message.content.upper().startswith('БРАТ'):
                await message.author.add_roles(roleKozak)
                await message.channel.send("Выдана роль " + str(roleKozak))
                await asyncio.sleep(0.5)
                await message.author.remove_roles(roleNelocal)
                await channel.purge(limit=100)
        if "Локальные" in rolenames:
            await message.channel.send("У тебя уже есть роль Локальные")
            await channel.purge(limit=100)
        else:
            if message.content.upper().startswith('КРАБОСТАН'):
                await message.author.add_roles(roleLocal)
                await message.channel.send("Выдана роль " + str(roleLocal))
                await asyncio.sleep(0.5)
                await message.author.remove_roles(roleNelocal)
                await channel.purge(limit=100)
    else:
        await bot.process_commands(message)

#Предупреждение
@bot.event
async def on_message(message):
	channel = bot.get_channel(333599055756132352)
	if message.channel.id == channel.id:
		await ctx.send("Для использования бота пишите в канал **bot_channel**")
		await channel.purge(limit=1)


# Очистка сообщений
@bot.command(pass_contex=True)
async def delyt(ctx, amount=1000):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=int(amount) + 1):
        messages.append(message)
    if ctx.message.author.id == 252824719764619264 or ctx.message.author.id == 432153138758287360:
        await channel.delete_messages(messages)
        await ctx.send('👌' + 'Удалены последние ' + str(amount) + ' сообщений', delete_after=1)

# Тест на пидора
@bot.command()
async def pidorcheck(ctx, member: discord.Member = None):
    channel = ctx.message.channel
    answers = [
        "**Мне кажется, или человек с именем** " + ctx.author.mention + " **по определению пидор?**🤔",
        member.mention + " **Ты Определенно пидор** 👌",
        member.mention + ", **Однозначно вы натурал** 😎",
        ctx.author.mention + " **А может ты пидор?**"
    ]
# f"{ctx.author} А может ты пидор?" - без упоминания
    message = random.choice(answers)
    #await channel.purge(limit=1)
    await ctx.send(message)

#Тест на пидора, но с табличками
@bot.command()
async def pdr2(ctx, member: discord.Member = None):
    channel = ctx.message.channel
    answers = [
        f"Мне кажется, или человек с именем **{ctx.author.name}** по определению пидор? 🤔",
        f"<:moon:334034106516242436> **{member.name}**, Однозначно вы натурал 😎",
        f"👌 Без сомнений, **{member.name}** пидор 👌 ",
        f"**{ctx.author.name}** А может ты пидор?"
    ]

    message = random.choice(answers)
    embed = discord.Embed(title = message,color = discord.Color.blue(),inline = True)

    #await channel.purge(limit=1)
    await ctx.send(embed=embed)

#Проверка платформы(хз зачем, но путсь будет)
@bot.command(aliases=['platform'])
async def plat(ctx):
    await ctx.send('Running on ' + sys.platform + ', python 3.6')

#Погода
@bot.command()
async def погода(ctx, city):
    channel = ctx.message.channel
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=fb1614a705527b4c51bba4cb79e40664&units=metric'.format(city)

    res = requests.get(url)
    data=res.json()
    embed = discord.Embed(colour=discord.Color.red())
    description = data['weather'][0]['description']
    #main = data['weather'][0]['main']
    icon = data['weather'][0]['icon']
    temp = data['main']['temp']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']

    embed.set_author(name='Какая сейчас погода в {}'.format(city))
    embed.add_field(name='Погодные условия', value=description, inline=False)
    embed.add_field(name='Температрура, ℃', value=temp, inline=True)
    embed.add_field(name='Давление, Па', value=pressure, inline=True)
    embed.add_field(name='Скорость ветра, м/c', value=wind_speed, inline=True)

    async with ctx.typing():
        await ctx.send('Получаю достоверную информацию...')
        await asyncio.sleep(2)
        await channel.purge(limit=1)
        await ctx.send(embed=embed)

#Intel
@bot.event
async def on_message(message):
    if message.content.startswith('=intel'):
        channel = message.channel
        embed = discord.Embed(title = '**Ну и зачем тебе Amude-геи, когда есть Intel-chan?**', colour=discord.Color.blue())

        embed.set_image(url='http://images.vfl.ru/ii/1546423781/5f5bcb33/24796066.jpg')
        embed.set_footer(text = str(message.author) + ' выбрал сторону синих', icon_url = message.author.avatar_url)

        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)

#Аватарка пользователя
@bot.command()
async def ava(ctx, member: discord.Member = None):
    await ctx.send(member.avatar_url)

# Комманда help
@bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour=discord.Color.green())

    embed.set_author(name='Список команд')
    embed.add_field(name='`=say сообщение`', value='Повторяет за вами сообщение', inline=False)
    embed.add_field(name='`=greet @упоминание`',value='Приветствует того, кого вы указали', inline=False)
    embed.add_field(name='`=delyt n, (n - целое число)`', value='Удаляет последние **n** сообщений', inline=False)
    embed.add_field(name='`=pidorcheck @упоминание`', value='Проводит тест на пидора', inline=False)
    embed.add_field(name='`=pdr2 @упоминание`', value='Проводит тест на пидора(вид таблички)', inline=False)
    #embed.add_field(name='`=pokemon имя`', value='Выводит полную информацию о данном покемоне', inline=False)
    embed.add_field(name='`=plat`', value='Выводит название платформы, на которой работает бот', inline=False)
    embed.add_field(name='`=погода (название города на *английском*)`', value='Выводит табличку с полным описанием погоды на данный момент в данном городе', inline=False)
    embed.add_field(name='`=intel`', value='Покажите ваше превосходство над amude-пидорами!', inline=False)
    embed.add_field(name='`=ava @упоминание`', value='Кидает прямую ссылку на аватарку пользователя', inline=False)

    await ctx.author.send(author, embed=embed)

@bot.command()
async def robotech_laws(ctx):
    await ctx.send("""1. роБ0т не может причинить вред человеку или своим бездействием допустить, чтобы человеку был причинён вред.""")
    await asyncio.sleep(0.5)
    await ctx.send("""2. роБ0т должен повиноваться всем приказам, которые даёт человек, кроме тех случаев, когда эти приказы противоречат Первому Закону.""")
    await asyncio.sleep(0.5)
    await ctx.send("""3. роБ0т должен заботиться о своей безопасности в той мере, в которой это не противоречит Первому или Второму Законам.""")


#Функция для рандомного статуса
async def chng_pr():
    status = ['=help для списка команд', 'Снизу пидор', 'discord.py v1.0','JS делает сас']
    await bot.wait_until_ready()
    status = ['=help для списка команд', 'Снизу пидор', 'discord.py v1.0','JS делает сас']

    while not bot.is_closed():
        curstat = random.choice(status)
        await bot.change_presence(activity = discord.Game(curstat))
        await asyncio.sleep(5)


# Logging
bot.loop.create_task(chng_pr())
bot.run(TOKEN)
