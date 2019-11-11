import discord
import datetime
from discord.ext import commands
import urllib.request
import json
import os
import time
import asyncio
import shutil

bot = commands.Bot(command_prefix = '$')


@bot.event
async def on_ready():
    print('Logged in --> Ready!')


@bot.event
async def on_guild_join(guild):
    global activeguildid
    global activeguildname
    print('resseting / initializing')
    if not os.path.exists(str(guild.name) + '_' + str(guild.id)):
        os.makedirs(str(guild.name) + '_' + str(guild.id))
    activeguildname = str(guild.name)
    activeguildid = str(guild.id)

    resetconfigfile()
    resetprivatechannelfile()
    resetpermissionsfile()


async def checkifsomeoneisinchannel(id, activeguildnametemp, activeguildidtemp, ctx):
    # timeout in minutes
    username = str(ctx.message.author.id)
    with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
        data = json.load(json_file)
    for p in data['Config']:
        timeout = p['timeoutvoice']
    timeout = int(timeout) * int(6)
    await asyncio.sleep(10)
    i = 0
    while timeout > i:
        #check if someone is in channel
        if bot.get_channel(int(id)) != None:
            if len(bot.get_channel(int(id)).members) != 0:
                i = 0
            else:
                i = i + 1
            await asyncio.sleep(10)
        else:
            print("channel deleted manually")
            i = timeout + 1
    if bot.get_channel(int(id)) != None:
        channel = bot.get_channel(int(id))
        await channel.delete()

        data = {}
        data['Voicechannels'] = []
        with open(activeguildnametemp + '_' + activeguildidtemp + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['ChannelID'] == str(id):
                    mychannels.remove(p)
                    Userschannel = 1

        if Userschannel == 1:

            with open(activeguildnametemp + '_' + activeguildidtemp + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            msg = await ctx.channel.send("<@" + username + "> Your private channel has been deleted due to inactivity")
            await asyncio.sleep(3)
            await msg.delete()


async def checkiftextchannelinuse(id, activeguildnametemp, activeguildidtemp, ctx):
    # timeout in minutes
    username = str(ctx.message.author.id)
    with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
        data = json.load(json_file)
    for p in data['Config']:
        timeout = p['timeouttext']

    timeoutja = True
    channel = bot.get_channel(int(id))
    while timeoutja:
        #check last message date/time
        if channel != None:
            await asyncio.sleep(10)
            lastmsg = await channel.history(limit=1).flatten()
            lastmymsg = await channel.fetch_message(int(lastmsg[0].id))

            if datetime.datetime.utcnow() > lastmymsg.created_at + datetime.timedelta(minutes=int(timeout)):
                timeoutja = False


        else:
            print("channel deleted manually")
    if bot.get_channel(int(id)) != None:
        channel = bot.get_channel(int(id))
        await channel.delete()

        data = {}
        data['Textchannels'] = []
        with open(activeguildnametemp + '_' + activeguildidtemp + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['ChannelID'] == str(id):
                    mychannels.remove(p)
                    Userschannel = 1

        if Userschannel == 1:

            with open(activeguildnametemp + '_' + activeguildidtemp + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            msg = await ctx.channel.send("<@" + username + "> Your private channel has been deleted due to inactivity")
            await asyncio.sleep(3)
            await msg.delete()


async def deletemsgdelay(dtime, msg):
    await asyncio.sleep(int(dtime))
    await msg.delete()


def getactiveguild(ctx):
    global activeguildid
    global activeguildname
    activeguildid = str(ctx.guild.id)
    activeguildname = str(ctx.guild.name)


def resetconfigfile():
    data = {}
    data['Config'] = []

    data['Config'].append({
        'privatecommandchannel': '',
        'privatecategory': '',
        'role': '',
        'timeouttext': '',
        'timeoutvoice': ''
    })
    with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    print("config reset complete")


def resetpermissionsfile():
    f = open(activeguildname + '_' + activeguildid + '/permissions.txt', 'w')
    f.close()
    print("permission reset complete")


def resetprivatechannelfile():
    data = {}
    data['Voicechannels'] = []
    data['Textchannels'] = []
    with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
        json.dump(data, outfile)
    print("channelconfig file reset complete ")


def readconfigfile(ctx):
    global commandchannelid
    global activeguildid
    global activeguildname
    global prvcategorychannelid
    print('active guild id:' + str(ctx.guild.id))
    getactiveguild(ctx)

    if not os.path.exists(activeguildname + '_' + activeguildid):
        os.makedirs(activeguildname + '_' + activeguildid)
    if not os.path.exists(activeguildname + '_' + activeguildid + '/settings.json'):
        open(activeguildname + '_' + activeguildid + '/settings.json', 'a').close()
        resetconfigfile()
        print("create file complete")
    if os.stat(activeguildname + '_' + activeguildid + '/settings.json').st_size == 0:
        resetconfigfile()

    with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
        data = json.load(json_file)
    for p in data['Config']:
        commandchannelid = p['privatecommandchannel']
        prvcategorychannelid = p['privatecategory']


@bot.command()
async def leaveserver(ctx):
    getactiveguild(ctx)
    global activeguildid
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            role = p['role']
        roles = []
        for s in ctx.message.author.roles:
            roles.append(int(s.id))
        print(roles)
        if int(role) in roles:
            print("Correct role")

            msg = await ctx.channel.send("Leaving the server now!")
            time.sleep(2)
            await msg.delete()
            print('delete msg queued')


            shutil.rmtree(activeguildname + '_' + activeguildid)
            guild = bot.get_guild(int(activeguildid))
            await guild.leave()


        else:
            print("wrong role or you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
    else:
        print("wrong channel")
        msg = await ctx.channel.send("This is the wrong channel")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')

@bot.command()
async def embeded(ctx, input):
    getactiveguild(ctx)
    pbf = urllib.request.urlopen(input)
    f = open("tempnews.txt", "w")
    # print(content)
    for linepb in pbf:
        linepb = linepb.decode("utf-8")
        linepb = linepb.replace("\n", "")
        f.write(str(linepb))
        print('write line')

    pbf.close()
    f.close()
    f = open("tempnews.txt", "r")
    line = f.readline()
    if not line.strip():
        await ctx.channel.send("title is required!")
    else:
        embededglobaltitle = line

        line = f.readline()
        if not line.strip():
            await ctx.channel.send("Color is required!")
        else:
            embededglobalcolor = line
            print(embededglobalcolor)

            line = f.readline()
            if not line.strip():
                globurlset = 0
            else:
                globurlset = 1
                embededglobalurl = line

            line = f.readline()
            if not line.strip():
                globdescription = 0
            else:
                globdescription = 1
                embededglobaldescription = line

            if globurlset == 1:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, timestamp = datetime.datetime.utcfromtimestamp(
                            datetime.datetime.timestamp(datetime.datetime.now())))
            else:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))

    line = f.readline()
    if not line.strip():
        print('no image')
    else:
        embededimageurl = line
        embed.set_image(url = embededimageurl)

    line = f.readline()
    if not line.strip():
        print('no thumbnail')
    else:
        embededthumbnailurl = line
        embed.set_thumbnail(url = embededthumbnailurl)

    line = f.readline()
    if not line.strip():
        print('no author')
        line = f.readline()
        line = f.readline()
    else:
        authorname = line

        line = f.readline()
        if not line.strip():
            print('no url')
            authorurlset = 0
        else:
            authorurl = line
            authorurlset = 1
        line = f.readline()
        if not line.strip():
            print('no iconurl')
            authoriconurlset = 0
        else:
            authoriconurl = line
            authoriconurlset = 1

        if authorurlset == 1:
            if authoriconurlset == 1:
                print('authurl + authiconurl')
                embed.set_author(name = authorname, url = authorurl, icon_url = authoriconurl)
            else:
                print('authurl')
                embed.set_author(name = authorname, url = authorurl)
        else:
            if authoriconurlset == 1:
                print('authiconurl')
                embed.set_author(name = authorname, icon_url = authoriconurl)
            else:
                print('authurl + authiconurl nicht')
                embed.set_author(name = authorname)

    line = f.readline()
    if not line.strip():
        print('no footer')
    else:
        footertext = line
        line = f.readline()
        if not line.strip():
            print('no icon footer url')
            embed.set_footer(text = footertext)
        else:
            footericonurl = line
            embed.set_footer(text = footertext, icon_url = footericonurl)
    num = 0
    for line in f:
        num = num + 1

        line = line.strip()

        line = line.split("'-'")
        print(line)
        line1 = line[0]
        line2 = line[1]
        line3 = line[2]

        if line3 == "0":
            line3 = ''

        if not line1.strip():
            await ctx.channel.send("Name is missing for area" + str(num) + "!!")
        else:
            if not line2.strip():
                if not line3.strip():
                    embed.add_field(name = line1, inline = True)
                    print("area" + str(num) + "name + inline")
                else:
                    embed.add_field(name = line1, inline = False)
                    print("area" + str(num) + "name")
            else:
                if not line3.strip():
                    embed.add_field(name = line1, value = line2, inline = True)
                    print("area" + str(num) + "name + value + inline")
                else:
                    embed.add_field(name = line1, value = line2, inline = False)
                    print("area" + str(num) + "name + value")

    print("for finished")
    await ctx.channel.send("News for @everyone")

    sent = await ctx.channel.send(embed = embed)
    await ctx.message.delete()
    await sent.add_reaction('\u274C')
    await sent.add_reaction('\u2705')

    f.close()

@bot.command()
async def freestuff(ctx, input):
    getactiveguild(ctx)
    pbf = urllib.request.urlopen(input)
    f = open("tempnews.txt", "w")
    # print(content)
    for linepb in pbf:
        linepb = linepb.decode("utf-8")
        linepb = linepb.replace("\n", "")
        f.write(str(linepb))
        print('write line')

    pbf.close()
    f.close()
    f = open("tempnews.txt", "r")
    line = f.readline()
    if not line.strip():
        await ctx.channel.send("title is required!")
    else:
        embededglobaltitle = line

        line = f.readline()
        if not line.strip():
            await ctx.channel.send("Color is required!")
        else:
            embededglobalcolor = line
            print(embededglobalcolor)

            line = f.readline()
            if not line.strip():
                globurlset = 0
            else:
                globurlset = 1
                embededglobalurl = line

            line = f.readline()
            if not line.strip():
                globdescription = 0
            else:
                globdescription = 1
                embededglobaldescription = line

            if globurlset == 1:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, timestamp = datetime.datetime.utcfromtimestamp(
                            datetime.datetime.timestamp(datetime.datetime.now())))
            else:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))

    line = f.readline()
    if not line.strip():
        print('no image')
    else:
        embededimageurl = line
        embed.set_image(url = embededimageurl)

    line = f.readline()
    if not line.strip():
        print('no thumbnail')
    else:
        embededthumbnailurl = line
        embed.set_thumbnail(url = embededthumbnailurl)

    line = f.readline()
    if not line.strip():
        print('no author')
        line = f.readline()
        line = f.readline()
    else:
        authorname = line

        line = f.readline()
        if not line.strip():
            print('no url')
            authorurlset = 0
        else:
            authorurl = line
            authorurlset = 1
        line = f.readline()
        if not line.strip():
            print('no iconurl')
            authoriconurlset = 0
        else:
            authoriconurl = line
            authoriconurlset = 1

        if authorurlset == 1:
            if authoriconurlset == 1:
                print('authurl + authiconurl')
                embed.set_author(name = authorname, url = authorurl, icon_url = authoriconurl)
            else:
                print('authurl')
                embed.set_author(name = authorname, url = authorurl)
        else:
            if authoriconurlset == 1:
                print('authiconurl')
                embed.set_author(name = authorname, icon_url = authoriconurl)
            else:
                print('authurl + authiconurl nicht')
                embed.set_author(name = authorname)

    line = f.readline()
    if not line.strip():
        print('no footer')
    else:
        footertext = line
        line = f.readline()
        if not line.strip():
            print('no icon footer url')
            embed.set_footer(text = footertext)
        else:
            footericonurl = line
            embed.set_footer(text = footertext, icon_url = footericonurl)
    num = 0
    for line in f:
        num = num + 1

        line = line.strip()

        line = line.split("'-'")
        print(line)
        line1 = line[0]
        line2 = line[1]
        line3 = line[2]

        if line3 == "0":
            line3 = ''

        if not line1.strip():
            await ctx.channel.send("Name is missing for area" + str(num) + "!!")
        else:
            if not line2.strip():
                if not line3.strip():
                    embed.add_field(name = line1, inline = True)
                    print("area" + str(num) + "name + inline")
                else:
                    embed.add_field(name = line1, inline = False)
                    print("area" + str(num) + "name")
            else:
                if not line3.strip():
                    embed.add_field(name = line1, value = line2, inline = True)
                    print("area" + str(num) + "name + value + inline")
                else:
                    embed.add_field(name = line1, value = line2, inline = False)
                    print("area" + str(num) + "name + value")

    print("for finished")

    sent = await ctx.channel.send(embed = embed)
    await ctx.message.delete()
    await sent.add_reaction('\u274C')
    await sent.add_reaction('\u2705')

    f.close()

@bot.command()
async def setcommandchannel(ctx):
    global activeguildid
    global activeguildname
    readconfigfile(ctx)
    getactiveguild(ctx)

    await ctx.message.delete()

    with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
        data = json.load(json_file)
    for p in data['Config']:
        role = p['role']
    roles = []
    for s in ctx.message.author.roles:
        roles.append(int(s.id))
    print(roles)
    if int(role) in roles:
        print("Correct role")

        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            p['privatecommandchannel'] = str(ctx.channel.id)

        with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
            json.dump(data, outfile, indent = 4)
        await ctx.channel.send("Command channel set to: " + " **" + str(bot.get_channel(ctx.channel.id).name) + "**")
    else:
        print("wrong role or you have no rights")
        msg = await ctx.channel.send("You don't have enough rights")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


@bot.command()
async def settimeouttext(ctx, input):
    getactiveguild(ctx)
    global activeguildid
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            role = p['role']
        roles = []
        for s in ctx.message.author.roles:
            roles.append(int(s.id))
        print(roles)
        if int(role) in roles:
            print("Correct role")
            with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
                data = json.load(json_file)
            for p in data['Config']:
                p['timeouttext'] = str(input)

            with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)

            msg = await ctx.channel.send("Timeout for Textchannels set to: " + " **" + str(input) + " minutes**")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            print("wrong role or you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
    else:
        print("wrong channel")
        msg = await ctx.channel.send("This is the wrong channel")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')

@bot.command()
async def settimeoutvoice(ctx, input):
    getactiveguild(ctx)
    global activeguildid
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            role = p['role']
        roles = []
        for s in ctx.message.author.roles:
            roles.append(int(s.id))
        print(roles)
        if int(role) in roles:
            print("Correct role")
            with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
                data = json.load(json_file)
            for p in data['Config']:
                p['timeoutvoice'] = str(input)

            with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)

            msg = await ctx.channel.send("Timeout for Voicechannels set to: " + " **" + str(input) + " minutes**")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            print("wrong role or you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
    else:
        print("wrong channel")
        msg = await ctx.channel.send("This is the wrong channel")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')

@bot.command()
async def setcategory(ctx, input):
    getactiveguild(ctx)
    global activeguildid
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            role = p['role']
        roles = []
        for s in ctx.message.author.roles:
            roles.append(int(s.id))
        print(roles)
        if int(role) in roles:
            print("Correct role")
            category = discord.utils.get(ctx.guild.channels,
                                         name = str(ctx.message.content.replace("$setcategory ", "")))
            with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
                data = json.load(json_file)
            for p in data['Config']:
                p['privatecategory'] = str(category.id)

            with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)

            await ctx.channel.send("Category set to: " + " **" + str(category.name) + "**")
        else:
            print("wrong role or you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
    else:
        print("wrong channel")
        msg = await ctx.channel.send("This is the wrong channel")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


@bot.command()
async def setrole(ctx, input):
    getactiveguild(ctx)
    global activeguildid
    readconfigfile(ctx)
    await ctx.message.delete()

    f = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
    if str(ctx.message.author) in f:
        print("User allowed")
        role = discord.utils.get(ctx.guild.roles,
                                 id = int(input.replace("<", '').replace("@", '').replace("&", '').replace(">", '')))
        print(role)
        with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
            data = json.load(json_file)
        for p in data['Config']:
            p['role'] = str(role.id)

        with open(activeguildname + '_' + activeguildid + '/settings.json', 'w') as outfile:
            json.dump(data, outfile, indent = 4)

        await ctx.channel.send("Allowed role set to: " + " **" + str(role.name) + "**")
    else:
        print("you have no rights to do that")
        msg = await ctx.channel.send("You don't have enough rights")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


@bot.command()
async def resetconfig(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        g = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
        if str(ctx.message.author) in g:
            print("User allowed")
            f = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
            with open(activeguildname + '_' + activeguildid + '/settings.json') as json_file:
                data = json.load(json_file)
            for p in data['Config']:
                role = p['role']
            roles = []
            for s in ctx.message.author.roles:
                roles.append(int(s.id))
            print(roles)
            if int(role) in roles or str(ctx.message.author) in f:
                print("Correct role")
                resetconfigfile()
                await ctx.channel.send("**CONFIG RESET COMPLETE**")
        else:
            print("you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def resetprvchannels(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        g = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
        if str(ctx.message.author) in g:
            print("User allowed")
            resetprivatechannelfile()
            print('searching for category with id: ' + prvcategorychannelid)
            category = bot.get_channel(int(prvcategorychannelid))
            print(category)
            print('----')
            for channel in category.channels:
                print(channel)
                if channel == bot.get_channel(int(commandchannelid)):
                    print("skipping commandchannel")
                else:
                    await channel.delete()

            print("Channels reset complete")
            msg = await ctx.channel.send("**Channels RESET COMPLETE**")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            print("wrong role or you have no rights")
            msg = await ctx.channel.send("You don't have enough rights")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def claim(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    if os.stat(activeguildname + '_' + activeguildid + '/permissions.txt').st_size == 0:
        f = open(activeguildname + '_' + activeguildid + '/permissions.txt', 'w')
        f.write(str(ctx.message.author))
        await ctx.channel.send("You have now the power over this bot")
    else:
        await ctx.channel.send("Someone already claimed!")
    f.close()


@bot.command()
async def claimadd(ctx, input):
    getactiveguild(ctx)
    readconfigfile(ctx)
    g = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
    if str(ctx.message.author) in g:
        print("User allowed")
        perm = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
        perm.append(str(bot.get_user(int(input.replace("!", '').replace("@", '').replace(">", '').replace("<", '')))))
        f = open(activeguildname + '_' + activeguildid + '/permissions.txt', 'w')
        for s in perm:
            f.write(str(s) + '\n')

        f.close()

        await ctx.channel.send("Added <@!" + str(bot.get_user(int(
            input.replace("!", '').replace("@", '').replace(">", '').replace("<", ''))).id) + "> to the approved list")
    else:
        print("you have no rights")
        msg = await ctx.channel.send("You don't have enough rights")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


@bot.command()
async def claimremove(ctx, input):
    getactiveguild(ctx)
    readconfigfile(ctx)
    g = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
    if str(ctx.message.author) in g:
        print("User allowed")
        perm = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
        perm.remove(str(bot.get_user(int(input.replace("!", '').replace("@", '').replace(">", '').replace("<", '')))))
        f = open(activeguildname + '_' + activeguildid + '/permissions.txt', 'w')
        for s in perm:
            f.write(str(s) + '\n')

        f.close()

        await ctx.channel.send("removed <@!" + str(bot.get_user(int(
            input.replace("!", '').replace("@", '').replace(">", '').replace("<",
                                                                             ''))).id) + "> from the approved list")

    else:
        print("have no rights")
        msg = await ctx.channel.send("You don't have enough rights")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


@bot.command()
async def claimreset(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    g = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
    if str(ctx.message.author) in g:
        print("User allowed")
        perm = open(activeguildname + '_' + activeguildid + '/permissions.txt').read().splitlines()
        f = open(activeguildname + '_' + activeguildid + '/permissions.txt', 'w')
        f.write(str(perm[0]))

        f.close()

        await ctx.channel.send("reset complete")
    else:
        print("have no rights")
        msg = await ctx.channel.send("You don't have enough rights")
        dtime = 2
        asyncio.create_task(deletemsgdelay(dtime, msg))
        print('delete msg queued')


# voicechannels:

@bot.command()
async def cv(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    name = str(ctx.message.content.replace("$cv ", "").replace("$cv", ""))
    if name.strip() != '':
        directname = True
    else:
        directname = False

    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        data = {}
        data['Voicechannels'] = []
        Userhaschannel = 0

        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            for p in data['Voicechannels']:
                print('User: ' + p['User'])
                print('ChannelName: ' + p['ChannelName'])
                print('ChannelID: ' + p['ChannelID'])
                print('-')
                if p['User'] == str(ctx.message.author):
                    Userhaschannel = 1

        print('--->End of channels file.')

        if Userhaschannel == 1:
            msg = await ctx.channel.send("You already created a private room!")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            if directname:
                channelname = name
            else:
                if ctx.message.author.nick is None:
                    channelname = str(ctx.message.author.name) + "'s room"
                else:
                    channelname = str(ctx.message.author.nick) + "'s room"

            channel = await ctx.guild.create_voice_channel(channelname, overwrite = True,
                                                           category = bot.get_channel(int(prvcategorychannelid)))
            # add permissoins to this channel
            await channel.set_permissions(ctx.message.author, read_messages = True)

            await channel.set_permissions(ctx.guild.default_role, read_messages = False)

            data['Voicechannels'].append({
                'User': str(ctx.message.author),
                'ChannelName': str(channel.name),
                'ChannelID': str(channel.id)
            })

            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            activeguildnametemp = activeguildname
            activeguildidtemp = activeguildid
            id = channel.id
            asyncio.create_task(checkifsomeoneisinchannel(id, activeguildnametemp, activeguildidtemp, ctx))
            print('created voicechannel + started timout delete task in background')


@bot.command()
async def dv(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    channelid = p['ChannelID']
                    mychannels.remove(p)
                    Userschannel = 1

        print('--->End of channels file.')

        if Userschannel == 1:
            msg = await ctx.channel.send("Deleting your private room!")
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            channel = bot.get_channel(int(channelid))
            await channel.delete()
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')

        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def rv(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        # check if user has a voice channel voice channel
        # rename voice channel
        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    p['ChannelName'] = str(ctx.message.content.replace("$rv ", ""))
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.edit(name = str(ctx.message.content.replace("$rv ", "")))
            msg = await ctx.channel.send("New name: **" + str(ctx.message.content.replace("$rv ", "")) + '**')
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')

@bot.command()
async def mvpu(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.set_permissions(ctx.guild.default_role, read_messages = True)
            msg = await ctx.channel.send("Your voicechannel is now public")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def mvpr(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.set_permissions(ctx.guild.default_role, read_messages = False)
            msg = await ctx.channel.send("Your voicechannel is now public")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def iuv(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))

            await channel.set_permissions(ctx.guild.get_member(int(ctx.message.mentions[0].id)), read_messages = True)
            msg = await ctx.channel.send("<@" + str(ctx.message.author.id) + "> added <@" + str(
                ctx.message.mentions[0].id) + "> to his/her channel")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def ruv(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))

            await channel.set_permissions(ctx.guild.get_member(int(ctx.message.mentions[0].id)), read_messages = False)
            msg = await ctx.channel.send("<@" + str(ctx.message.author.id) + "> removed <@" + str(
                ctx.message.mentions[0].id) + "> from his/her channel")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def rvd(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Voicechannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Voicechannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    channelid = p['ChannelID']
                    mychannels.remove(p)
                    Userschannel = 1

        print('--->End of channels file.')

        if Userschannel == 1:
            msg = await ctx.channel.send("Voicechannel reset to default")
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            channel = bot.get_channel(int(channelid))
            await channel.delete()

            if ctx.message.author.nick is None:
                channelname = str(ctx.message.author.name) + "'s room"
            else:
                channelname = str(ctx.message.author.nick) + "'s room"

            channel = await ctx.guild.create_voice_channel(channelname, overwrite = True,
                                                           category = bot.get_channel(int(prvcategorychannelid)))
            # add permissoins to this channel
            await channel.set_permissions(ctx.message.author, read_messages = True)

            await channel.set_permissions(ctx.guild.default_role, read_messages = False)

            data['Voicechannels'].append({
                'User': str(ctx.message.author),
                'ChannelName': str(channel.name),
                'ChannelID': str(channel.id)
            })

            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)

            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')



        else:
            msg = await ctx.channel.send("You have to create a channel first")

            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')

# end voicechannels
# textchannels

@bot.command()
async def ct(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    name = str(ctx.message.content.replace("$ct ", "").replace("$ct", ""))
    if name.strip() != '':
        directname = True
    else:
        directname = False

    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        data = {}
        data['Textchannels'] = []
        Userhaschannel = 0

        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            for p in data['Textchannels']:
                print('User: ' + p['User'])
                print('ChannelName: ' + p['ChannelName'])
                print('ChannelID: ' + p['ChannelID'])
                print('-')
                if p['User'] == str(ctx.message.author):
                    Userhaschannel = 1

        print('--->End of channels file.')

        if Userhaschannel == 1:
            msg = await ctx.channel.send("You already created a private room!")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            if directname:
                channelname = name
            else:
                if ctx.message.author.nick is None:
                    channelname = str(ctx.message.author.name) + "'s room"
                else:
                    channelname = str(ctx.message.author.nick) + "'s room"

            channel = await ctx.guild.create_text_channel(channelname, overwrite = True, category = bot.get_channel(int(prvcategorychannelid)))
            await channel.send("<@" + str(ctx.message.author.id) + "> This is your private place.")
            # add permissoins to this channel
            await channel.set_permissions(ctx.message.author, read_messages = True)

            await channel.set_permissions(ctx.guild.default_role, read_messages = False)

            data['Textchannels'].append({
                'User': str(ctx.message.author),
                'ChannelName': str(channel.name),
                'ChannelID': str(channel.id)
            })

            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            activeguildnametemp = activeguildname
            activeguildidtemp = activeguildid
            id = channel.id
            asyncio.create_task(checkiftextchannelinuse(id, activeguildnametemp, activeguildidtemp, ctx))
            print('created textchannel + started timout delete task in background')


@bot.command()
async def dt(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)

    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")
        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    channelid = p['ChannelID']
                    mychannels.remove(p)
                    Userschannel = 1

        print('--->End of channels file.')

        if Userschannel == 1:
            msg = await ctx.channel.send("Deleting your private room!")
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            channel = bot.get_channel(int(channelid))
            await channel.delete()
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')

        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def rt(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        # check if user has a voice channel voice channel
        # rename voice channel
        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    p['ChannelName'] = str(ctx.message.content.replace("$rt ", ""))
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.edit(name = str(ctx.message.content.replace("$rt ", "")))
            msg = await ctx.channel.send("New name: **" + str(ctx.message.content.replace("$rt ", "")) + '**')
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def mtpu(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.set_permissions(ctx.guild.default_role, read_messages = True)
            msg = await ctx.channel.send("Your voicechannel is now public")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def mtpr(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        print('--->End of channels file.')

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))
            await channel.set_permissions(ctx.guild.default_role, read_messages = False)
            msg = await ctx.channel.send("Your voicechannel is now public")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def iut(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))

            await channel.set_permissions(ctx.guild.get_member(int(ctx.message.mentions[0].id)), read_messages = True)
            msg = await ctx.channel.send("<@" + str(ctx.message.author.id) + "> added <@" + str(ctx.message.mentions[0].id) + "> to his/her channel")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def rut(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    Userschannel = 1
                    channelid = p['ChannelID']

        if Userschannel == 1:
            channel = bot.get_channel(int(channelid))

            await channel.set_permissions(ctx.guild.get_member(int(ctx.message.mentions[0].id)), read_messages = False)
            msg = await ctx.channel.send("<@" + str(ctx.message.author.id) + "> removed <@" + str(ctx.message.mentions[0].id) + "> from his/her channel")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')
        else:
            msg = await ctx.channel.send("You have to create a channel first")
            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


@bot.command()
async def rtd(ctx):
    getactiveguild(ctx)
    readconfigfile(ctx)
    print("config for commandchannel : " + str(commandchannelid))
    await ctx.message.delete()
    if str(ctx.channel.id) == commandchannelid:  # Check if in correct channel
        print("Correct channel")

        data = {}
        data['Textchannels'] = []
        with open(activeguildname + '_' + activeguildid + '/channeldata.json') as json_file:
            data = json.load(json_file)
            print('--->Start of channels file.')
            mychannels = data['Textchannels']
            Userschannel = 0
            for p in mychannels:
                if p['User'] == str(ctx.message.author):
                    channelid = p['ChannelID']
                    mychannels.remove(p)
                    Userschannel = 1

        print('--->End of channels file.')

        if Userschannel == 1:
            msg = await ctx.channel.send("Voicechannel reset to default")
            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)
            channel = bot.get_channel(int(channelid))
            await channel.delete()

            if ctx.message.author.nick is None:
                channelname = str(ctx.message.author.name) + "'s room"
            else:
                channelname = str(ctx.message.author.nick) + "'s room"

            channel = await ctx.guild.create_voice_channel(channelname, overwrite = True, category = bot.get_channel(int(prvcategorychannelid)))
            # add permissoins to this channel
            await channel.set_permissions(ctx.message.author, read_messages = True)

            await channel.set_permissions(ctx.guild.default_role, read_messages = False)

            data['Textchannels'].append({
                'User': str(ctx.message.author),
                'ChannelName': str(channel.name),
                'ChannelID': str(channel.id)
            })

            with open(activeguildname + '_' + activeguildid + '/channeldata.json', 'w') as outfile:
                json.dump(data, outfile, indent = 4)

            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')



        else:
            msg = await ctx.channel.send("You have to create a channel first")

            dtime = 2
            asyncio.create_task(deletemsgdelay(dtime, msg))
            print('delete msg queued')


# end textchannels

bot.remove_command('help')  # remove standart help

@bot.command()
async def initbot(ctx):
    global activeguildid
    global activeguildname
    getactiveguild(ctx)
    await ctx.message.delete()
    print('resseting / initializing')
    if not os.path.exists(str(ctx.guild.name) + '_' + str(ctx.guild.id)):
        os.makedirs(str(ctx.guild.name) + '_' + str(ctx.guild.id))
    activeguildname = str(ctx.guild.name)
    activeguildid = str(ctx.guild.id)

    resetconfigfile()
    resetprivatechannelfile()
    resetpermissionsfile()
    msg = await ctx.channel.send("bot has been reinitialized")
    dtime = 2
    asyncio.create_task(deletemsgdelay(dtime, msg))
    print('delete msg queued')

@bot.command()
async def help(ctx):
    getactiveguild(ctx)

    f = open(activeguildname + '_' + activeguildid + "/help.txt", "r")
    line = f.readline()
    if not line.strip():
        await ctx.channel.send("title is required!")
    else:
        embededglobaltitle = line

        line = f.readline()
        if not line.strip():
            await ctx.channel.send("Color is required!")
        else:
            embededglobalcolor = line
            print(embededglobalcolor)

            line = f.readline()
            if not line.strip():
                globurlset = 0
            else:
                globurlset = 1
                embededglobalurl = line

            line = f.readline()
            if not line.strip():
                globdescription = 0
            else:
                globdescription = 1
                embededglobaldescription = line

            if globurlset == 1:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          url = embededglobalurl, timestamp = datetime.datetime.utcfromtimestamp(
                            datetime.datetime.timestamp(datetime.datetime.now())))
            else:
                if globdescription == 1:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          description = embededglobaldescription,
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))
                else:
                    embed = discord.Embed(title = embededglobaltitle, colour = discord.Colour(0xffffff),
                                          timestamp = datetime.datetime.utcfromtimestamp(
                                              datetime.datetime.timestamp(datetime.datetime.now())))

    line = f.readline()
    if not line.strip():
        print('no image')
    else:
        embededimageurl = line
        embed.set_image(url = embededimageurl)

    line = f.readline()
    if not line.strip():
        print('no thumbnail')
    else:
        embededthumbnailurl = line
        embed.set_thumbnail(url = embededthumbnailurl)

    line = f.readline()
    if not line.strip():
        print('no author')
        line = f.readline()
        line = f.readline()
    else:
        authorname = line

        line = f.readline()
        if not line.strip():
            print('no url')
            authorurlset = 0
        else:
            authorurl = line
            authorurlset = 1
        line = f.readline()
        if not line.strip():
            print('no iconurl')
            authoriconurlset = 0
        else:
            authoriconurl = line
            authoriconurlset = 1

        if authorurlset == 1:
            if authoriconurlset == 1:
                print('authurl + authiconurl')
                embed.set_author(name = authorname, url = authorurl, icon_url = authoriconurl)
            else:
                print('authurl')
                embed.set_author(name = authorname, url = authorurl)
        else:
            if authoriconurlset == 1:
                print('authiconurl')
                embed.set_author(name = authorname, icon_url = authoriconurl)
            else:
                print('authurl + authiconurl nicht')
                embed.set_author(name = authorname)

    line = f.readline()
    if not line.strip():
        print('no footer')
    else:
        footertext = line
        line = f.readline()
        if not line.strip():
            print('no icon footer url')
            embed.set_footer(text = footertext)
        else:
            footericonurl = line
            embed.set_footer(text = footertext, icon_url = footericonurl)
    num = 0
    for line in f:
        num = num + 1

        line = line.strip()

        line = line.split("'-'")
        print(line)
        line1 = line[0]
        line2 = line[1]
        line3 = line[2]

        if line3 == "0":
            line3 = ''

        if not line1.strip():
            await ctx.channel.send("Name is missing for area" + str(num) + "!!")
        else:
            if not line2.strip():
                if not line3.strip():
                    embed.add_field(name = line1, inline = True)
                    print("area" + str(num) + "name + inline")
                else:
                    embed.add_field(name = line1, inline = False)
                    print("area" + str(num) + "name")
            else:
                if not line3.strip():
                    embed.add_field(name = line1, value = line2, inline = True)
                    print("area" + str(num) + "name + value + inline")
                else:
                    embed.add_field(name = line1, value = line2, inline = False)
                    print("area" + str(num) + "name + value")

    print("for finished")

    msg = await ctx.channel.send(embed = embed)
    await ctx.message.delete()
    dtime = 300
    asyncio.create_task(deletemsgdelay(dtime, msg))
    print('delete msg queued')

    f.close()

@bot.command()
async def sethelp(ctx, input):
    getactiveguild(ctx)
    pbf = urllib.request.urlopen(input)
    f = open(activeguildname + '_' + activeguildid + "/help.txt", "w")
    # print(content)
    for linepb in pbf:
        linepb = linepb.decode("utf-8")
        linepb = linepb.replace("\n", "")
        f.write(str(linepb))
        print('write line')

    pbf.close()
    f.close()

    await ctx.channel.send("Help updated")

    await ctx.message.delete()

Token = str(open('Token.txt', 'r').read())
bot.run(Token)

# Todo: -move user to channel
# Todo: -delete voice / text individually