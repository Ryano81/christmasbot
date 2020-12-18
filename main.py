# bot.py

import discord
import datetime
import random
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True  # This line is required to get member ID's

TOKEN = 'NzgwOTA1Mjc2Mjk0NDMwNzQw.X714tg.kMU2X2IIue4aqsqbA5n3S0AQPgM'
GUILD = '723977864373862451'

client = discord.Client(intents=intents)


def gettime(t):  # Main time calculating function
    dt = datetime.datetime
    now = dt.now()
    delta = dt(year=2020, month=12, day=25, hour=0, minute=0, second=0) - dt(year=now.year, month=now.month,
                                                                             minute=now.minute, day=now.day,
                                                                             hour=now.hour, second=now.second)
    if delta.seconds < 0 or delta.days < 0:
        return 0
    else:
        sdelta = str(delta)
        dif1 = str.replace(sdelta, " ", "")
        dif2 = str.replace(dif1, "days,", "")
        dif3 = datetime.datetime.strptime(dif2, "%d%H:%M:%S")
        if t == "day":
            return dif3.day
        elif t == "hour":
            return dif3.hour
        elif t == "second":
            return dif3.second
        elif t == "minute":
            return dif3.minute
        elif t == "tsecond":  # returns total seconds left
            return delta.total_seconds()


@client.event
async def on_ready():  # Prints whatever guilds the bot is a part of for debug purposes.
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        game = discord.Game("?help")
        await client.change_presence(status=discord.Status.online, activity=game)


@tasks.loop(minutes=5)  # This task just changes reid's name periodically because he asked me to do that
async def reid_nick():
    await client.wait_until_ready()
    guild = client.get_guild(723977864373862451)
    reid = guild.get_member(404418819574988800)
    nickname = str(round(gettime('tsecond')))
    await reid.edit(nick=nickname)
    print(str(datetime.datetime.now()) + " : " + "Reid's nickname was changed")


@tasks.loop(hours=24)  # loops every day
async def daily_announcement():
    channel = client.get_channel(724813963207901245)
    await channel.send('There are now ' + str(gettime("day")) + ' days until Christmas!')
    print("message sent")


@daily_announcement.before_loop  # This task just waits until 12:00 ECT and then runs the next one daily_announcement
async def before_daily_announcement():
    time_for_thing_to_happen = datetime.time(hour=5)  # this is in UTC, it is 5 hours ahead of est
    now = datetime.datetime.utcnow()
    date = now.date()
    if now.time() > time_for_thing_to_happen:
        date = now.date() + datetime.timedelta(days=1)
    then = datetime.datetime.combine(date, time_for_thing_to_happen)
    print(str("waiting until " + str(then) + ' it is now ' + str(now)))
    await discord.utils.sleep_until(then)


@client.event
async def on_message(message):  # This whole function just checks for specific phrases.
    if message.author == client.user:
        return

    if message.content == '?help' or message.content == '?Help':
        # change this everytime you add a command, added a new embed
        embed = discord.Embed(
            title='List of commands:',
            color=discord.Colour.blue(),
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/780905276294430740'
                                '/92c57faee58f726be6461ad685eb85f2.png?size=256')
        embed.add_field(name='?help:', value='The page that you are looking at now.', inline=True)
        embed.add_field(name='?count:', value='Returns the time left until Christmas.', inline=True)
        embed.add_field(name='?scount:', value='Returns the time left until Christmas in seconds.', inline=True)
        embed.add_field(name='?mcount:', value='Returns the time left until Christmas in minutes.', inline=True)
        embed.add_field(name='?hcount:', value='Returns the time left until Christmas in hours.', inline=True)
        embed.add_field(name='?joke:', value='Sends a random christmas joke.', inline=True)
        embed.add_field(name='?code:', value='sends a link to the source code', inline=True)
        embed.set_footer(text='Bot made by RyanO8#0001')
        await message.channel.send(embed=embed)
        guild = message.guild
        guildname = guild.name
        print(str(datetime.datetime.now()) + " : " + guildname + " : " + 'Someone asked for help')

    if message.content == '?count' or message.content == '?Count':
        # Checks if christmas has passed
        if gettime("day") == 0:
            await message.channel.send("Merry Christmas!")
            print(str(datetime.datetime.now()) + " : " + 'Merry Christmas!')
        else:
            response = str("Christmas is in " + str(gettime("day")) + " days " + str(gettime("hour")) + " hours " +
                           str(gettime("minute")) + " minutes and " + str(gettime('second')) + ' seconds')
            await message.channel.send(response)
            guild = message.guild
            guildname = guild.name
            print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)

    if message.content == '?scount' or message.content == '?Scount':
        if gettime('day') == 0:
            await message.channel.send('Merry Christmas!')
            print(str(datetime.datetime.now()) + " : " + "Merry Christmas!")
        else:
            response = str("There are " + str(int(gettime("tsecond"))) + ' total seconds until Christmas!')
            await message.channel.send(response)
            guild = message.guild
            guildname = guild.name
            print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)

    if message.content == '?mcount' or message.content == '?Mcount':
        if gettime('day') == 0:
            await message.channel.send('Merry Christmas!')
            print(str(datetime.datetime.now()) + " : " + "Merry Christmas!")
        else:
            minutes = round((int(gettime('tsecond')) / 60), 2)
            response = str("There are " + str(minutes) + ' total minutes until Christmas!')
            await message.channel.send(response)
            guild = message.guild
            guildname = guild.name
            print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)

    if message.content == '?hcount' or message.content == '?Hcount':
        if gettime('day') == 0:
            await message.channel.send('Merry Christmas!')
            print(str(datetime.datetime.now()) + " : " + "Merry Christmas!")
        else:
            hours = round((int(gettime('tsecond')) / 3600), 2)
            response = str("There are " + str(hours) + ' total hours until Christmas!')
            await message.channel.send(response)
            guild = message.guild
            guildname = guild.name
            print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)

    if message.content == '?joke' or message.content == '?Joke':
        jokes = ["What does Santa suffer from if he gets stuck in a chimney? \nClaus-trophobia!",

                 "What happened to the man who stole an Advent Calendar? \nHe got 25 days!",

                 "What do they sing at a snowman’s birthday party? \nFreeze a jolly good fellow!",

                 "What do Santa’s little helpers learn at school? \nThe elf-abet!",

                 "What kind of motorbike does Santa ride? \nA Holly Davidson!",

                 "What did Santa do when he went speed dating? \nHe pulled a cracker!",

                 "Why was the turkey in the pop group? \nBecause he was the only one with drumsticks!",

                 "What do you get if you cross Santa with a duck? \nA Christmas Quacker!",

                 "What goes “Oh, Oh, Oh”? \nSanta walking backwards!",

                 "Why was the snowman looking through the carrots? \nHe was picking his nose!",

                 "Why does Santa have three gardens? \nSo he can ‘ho ho ho’!",

                 "What is the best Christmas present in the world? \nA broken drum, you just can’t beat it!",

                 "What do snowmen wear on their heads? \nIce caps!",

                 "What did Adam say the day before Christmas? \n“It’s Christmas, Eve!”",

                 "What do you get when you cross a snowman with a vampire? \nFrostbite!",

                 "What did the stamp say to the Christmas card? \nStick with me and we’ll go places!",

                 "What does the Queen call her Christmas Broadcast? \nThe One Show!",

                 "Why don’t you ever see Santa in hospital? \nBecause he has private elf care!",

                 "How did Mary and Joseph know Jesus’ weight when he was born? \nThey had a weigh in a manger!",

                 "Why is it getting harder to buy Advent calendars? \nTheir days are numbered!",

                 "How did Scrooge win the football game? \nThe ghost of Christmas passed!",

                 "What do angry mice send to each other at Christmas? \nCross-mouse cards!",

                 "What do you call a bunch of chess players bragging about their games in a hotel lobby? \nChess nuts "
                 "boasting in an open foyer!",

                 "What did the beaver say to the Christmas Tree? \nNice gnawing you!",

                 "What does Miley Cyrus have at Christmas? \nTwerky!",

                 "What does Santa do with out of shape elves? \nSends them to an elf Farm.",

                 "Why did Santa’s helper see the doctor? \nBecause he had a low “elf” esteem!",

                 "Who hides in the bakery at Christmas? \nA mince spy!",

                 "How do snowmen get around? \nThey ride an icicle!",

                 "What do snowmen have for breakfast? \nSnowflakes!",

                 "What does Santa do when his elves misbehave? \nHe gives them the sack!",

                 "What did Santa say to the smoker? \nPlease don’t smoke, it’s bad for my elf!",

                 "What do you get if you eat Christmas decorations? \nTinsilitis!",

                 "What’s the most popular Christmas wine? \n'But I don’t like Brussels sprouts!'",

                 "What’s green, covered in tinsel and goes ribbet ribbet? \nA mistle-toad!",

                 "Which famous playwright was terrified of Christmas? \nNoël Coward!",

                 "What carol is heard in the desert? \n‘O camel ye faithful!’",

                 "How many letters are in the Christmas alphabet? \nOnly 25, there’s no L!",

                 "What do reindeer hang on their Christmas trees? \nHorn-aments!",

                 "Why are Christmas trees so bad at sewing? \nThey always drop their needles!",

                 "How will Christmas dinner be different after Brexit? \nNo Brussels!",

                 "How does Christmas Day end? \nWith the letter Y!",

                 "What happened to the turkey at Christmas? \nIt got gobbled!",

                 "What do snowmen eat for lunch? \nIcebergers!",

                 "When is a boat just like snow? \nWhen it’s adrift!",

                 "Who delivers presents to cats? \nSanta Paws!",

                 "Why did the turkey cross the road? \nBecause it was the chicken’s day off!",

                 "What do you get if you cross Santa with a detective? \nSanta Clues!",

                 "What goes Ho Ho Whoosh, Ho Ho Whoosh? \nSanta going through a revolving door!",

                 "What is Santa’s favourite place to deliver presents? \nIdaho-ho-ho!",

                 "What do you call buying a piano for the holidays? \nChristmas Chopin!",

                 "What’s a child’s favourite king at Christmas? \nA stoc-king!",

                 "Who is Santa’s favourite singer? \nElf-is Presley!",

                 "Why couldn’t the skeleton go to the Christmas Party? \nBecause he had no body to go with!",

                 "How does Darth Vader enjoy his Christmas Turkey? \nOn the dark side!",

                 "Who’s Rudolph’s favourite pop star? \nBeyon-sleigh!",

                 "What do monkeys sing at Christmas? \nJungle bells!",

                 "Who do Santa’s helpers call when they’re ill? \nThe National Elf Service!",

                 "What is white and minty? \nA polo bear!",

                 "Why did Scrooge keep a pet lamb? \nBecause it would say, “Baaaaahh humbug!”",

                 "Who is a Christmas tree’s favorite singer? \nSpruce Springsteen!",

                 "What cars do elves drive? \nToyotas!",

                 "What is Santa’s primary language? \nNorth Polish.",

                 "What do reindeer say before they tell a joke? \nThis one will sleigh you!",

                 "How do you lift a frozen car? \nWith a Jack Frost!",

                 "Which holiday mascot has the least spare change? \nSt. Nickel-less!",

                 "What would you call an elf who just has won the lottery? \nWelfy!",

                 "How did the bauble get addicted to Christmas? \nHe was hooked on trees his whole life!",

                 "What do you call an obnoxious reindeer? \nRude-olph!",

                 "Why are Christmas trees so fond of the past? \nBecause the present’s beneath them!",

                 "What do you call a kid who doesn’t believe in Santa? \nA rebel without a Claus!",

                 "Why does Santa go down the chimney? \nBecause it soots him!",

                 "Why did Santa get a parking ticket on Christmas Eve? \nHe left his sleigh in a snow parking zone!",

                 "What do you call Santa living at the South Pole? \nA lost clause!",

                 "What part of the body do you only see during Christmas? \nMistletoe!",

                 "What do the elves cook with in the kitchen? \nUtinsels!",

                 "What’s the difference between Santa Clause and a knight? \nOne slays a dragon, the other drags a "
                 "sleigh!",

                 "What do you call cutting down a Christmas tree? \nChristmas chopping!",

                 "Where do Santa and his reindeer go to get hot chocolate while flying in the sky? \nStar-bucks.",

                 "What do sheep say at Christmas? \nA Merry Christmas to Ewe!",

                 "Why is everyone so thirsty at the north pole? \nThere’s no well, no well!",

                 "Which football team did the baby Jesus support? \nManger-ster United!",

                 "What do you get if you cross a Christmas tree with an apple? \nA pineapple!",

                 "Why is winter a snowman’s favourite time of year? \nBecause they can camouflage!",

                 "What do vampires sing on New Year’s Eve? \nAuld Fang Syne!",

                 "What athlete is warmest in winter? \nA long jumper!",

                 "What do you get if you cross a bell with a skunk? \nJingle Smells!",

                 "What do you get when you cross a deer with rain? \nA reindeer!",

                 "What’s worse than Rudolph with a runny nose? \nFrosty the Snowman with a hot flush!",

                 "What is the most competitive season? \nWin-ter!",

                 "What type of key do you need for a Nativity play? \nA don-key!",

                 "Why don’t penguins fly? \nBecause they’re not tall enough to be pilots!",

                 "What did the Christmas tree say to the ornament? \nQuit hanging around!",

                 "Why wouldn't the cat climb the Christmas tree? \nIt was afraid of the bark.",

                 "Why was Theresa May sacked as nativity manager? \nShe couldn’t run a stable government!",

                 "Why don’t Southern Rail train guards share advent calendars? \nThey want to open the doors "
                 "themselves!",

                 "What’s the difference between Spirit Airlines and Santa? \nSanta flies at least once a year!",

                 "Kim Jong Un will play Santa this year in the South’s annual pantomime. \nHe said he fancied a Korea "
                 "change!",

                 "How does a monkey celebrate Christmas? \n by singing jungle bells!"

                 ]
        length = len(jokes) - 1
        response = jokes[random.randint(0, length)]
        await message.channel.send(response)
        guild = message.guild
        guildname = guild.name
        print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)

    if message.content == '?code' or message.content == '?Code':
        response = 'https://hastebin.com/erofoziham.py'
        await message.channel.send(response)
        guild = message.guild
        guildname = guild.name
        print(str(datetime.datetime.now()) + " : " + guildname + " : " + response)


# This just calls the functions from before
reid_nick.start()
daily_announcement.start()

client.run(TOKEN)
