
# -*- coding: utf8 -*-
import asyncio
import random
from time import strftime

import discord
from discord.ext import commands
import wikipedia
import requests
import tools.discordembed as dmbd



class Fun:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, *, dice: str ='1d6'):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await self.bot.say('Format has to be in NdN!')
            return

        author = ctx.message.author
        title = 'Here are your dice results!'
        em = dmbd.newembed(author, title)
        for r in range(rolls):
            em.add_field(name="Dice #" + str(r+1), value=str(random.randint(1, limit)))
        # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('roll')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flips a coin."""
        author = ctx.message.author
        em = dmbd.newembed(author)
        coin = random.randint(1, 2)
        if coin == 1:
            em.set_image(url="https://www.usmint.gov/wordpress/wp-content/uploads/2017/03/2017-lincoln-penny-uncirculated-reverse-300x300.jpg")
            await self.bot.say(embed=em)
        elif coin == 2:
            em.set_image(url="https://www.usmint.gov/wordpress/wp-content/uploads/2017/03/2017-lincoln-penny-proof-obverse-san-francisco-300x300.jpg")
            await self.bot.say(embed=em)

        self.bot.cogs['WordDB'].cmdcount('flip')

    @commands.command(pass_context=True)
    async def wiki(self, ctx, *, search: str):
        """ Grabs Wikipedia Article """
        searchlist = wikipedia.search(search)
        if len(searchlist) < 1:
            author = ctx.message.author
            title = "Searched for: " + search
            desc = 'No Results Found'
            em = dmbd.newembed(author, title, desc)
            await self.bot.say(embed=em)
        else:
            page = wikipedia.page(searchlist[0])

            author = ctx.message.author
            title = page.title
            desc = wikipedia.summary(searchlist[0], 3)
            url = page.url
            em = dmbd.newembed(author, title, desc, url)

            em.set_image(url=page.images[0])
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/250px-Wikipedia-logo-v2-en.svg.png")
            self.bot.cogs['WordDB'].cmdcount('wiki')
            await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def ask(self, ctx, *, s: str):
        """ Asks wolfram alpha"""
        s.replace(' ', '+')
        req = requests.get("http://api.wolframalpha.com/v1/result?appid=RPYQ54-Q3W9QJKWR9&i=" + s)
        author = ctx.message.author
        em = dmbd.newembed(author, req.text)
        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('ask')


    @commands.command(pass_context=True, description='Ask the Bot to choose one')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        author = ctx.message.author
        em = dmbd.newembed(author, random.choice(choices))
        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('choose')

    @commands.command(pass_context=True, name='8ball')
    async def ball(self, ctx):
        """ Ask the 8Ball """
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
                   'Yes, definitely', 'You may rely on it', 'As I see it, yes',
                   'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                   'Reply hazy try again', 'Ask again later',
                   'Better not tell you now', 'Cannot predict now',
                   'Concentrate and ask again', 'Don\'t count on it',
                   'My reply is no', 'My sources say no',
                   'Outlook not so good', 'Very doubtful']

        author = ctx.message.author
        em = dmbd.newembed(author, random.choice(answers))
        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('8ball')


    @commands.command(pass_context=True)
    async def avatar(self, ctx, *, name: str):
        """ Grabbing an avatar of a person """
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.server.get_member_named(name)
        if not user:
            name = name.lower()
            for x in ctx.message.server.members:
                if x.name.lower() == name:
                    user = x
                elif x.nick:
                    if x.nick.lower() == name:
                        user = x

        if not user:
            return
        author = ctx.message.author
        em = dmbd.newembed(author, u=user.avatar_url)
        em.set_image(url=user.avatar_url)
        grade = random.randint(1,11)
        em.add_field(name=user.name + '#' + user.discriminator + '\'s Avatar', value=str(grade) + "/10")

        await self.bot.say(embed=em)
        self.bot.cogs['WordDB'].cmdcount('avatar')


    @commands.command()
    async def brainpower(self):
        """ ADRENALINE IS PUMPING """
        await self.bot.say("O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo " +
                           "AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-" +
                           " JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA")
        self.bot.cogs['WordDB'].cmdcount('brainpower')

def setup(bot):
    bot.add_cog(Fun(bot))
