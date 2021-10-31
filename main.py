from sql import *
from functions import *
import discord
from discord.ext import commands
from table import *

RoleList = ["Top 10", "Top 100", "Top 500", "Top 1000", "Top 2000", "Top 3000", "Top 4000", "Top 5000", "Over 5000"]
RoleLocal = [10, 100, 500, 1000, 2000, 3000, 4000, 5000]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = 'r!', intents=intents)

@bot.command(pass_context = True)
@commands.has_role('Tourney Admins')
async def SetupRoles(ctx):
    global RoleList

    for i in RoleList:
        if discord.utils.get(ctx.guild.roles, name=i):
            continue
        else:
            await ctx.guild.create_role(name=i, colour=discord.Colour(0x0062ff))

@bot.command(pass_context=True)
@commands.has_role('Tourney Admins')
async def AddToDB(ctx, arg1, arg2):
    member = ctx.guild.get_member_named(arg1)
    if(member == None):
        await addToDatabase('"' + arg1 + '"', '"' + arg2 + '"')
    else:
        await addToDatabase('"' + str(member.id) + '"', '"' + arg2 + '"')

@bot.command(pass_context=True)
@commands.has_role('Tourney Admins')
async def UpdateAllRanks(ctx):
    global RoleList
    global RoleLocal
    guild = ctx.guild

    List = await getAll()

    for i in List:
        try:
            member = guild.get_member(int(list(i)[0]))
        except:
            member = guild.get_member_named(list(i)[0])
            
        rank = await checkRank(list(i)[1])
        val = await checkRolesWithRank(rank, RoleLocal)
        
        if (val == "Null"):
            continue
        else:

            for r in RoleList:
                try:
                    role = discord.utils.get(guild.roles, r)
                    await member.remove_roles(role)
                except:
                    continue

            role = discord.utils.get(guild.roles, name=RoleList[val])
            await member.add_roles(role)

@bot.command(pass_context=True)
@commands.has_role('Tourney Admins')
async def UpdateElo(ctx, arg1, arg2):
    winnerM = ctx.guild.get_member_named(arg1)
    loserM = ctx.guild.get_member_named(arg2)
    
    if (winnerM != None):
        winnerElo = await getUserElo( '"' + str(winnerM.id) + '"')
    else:
        winnerElo = await getUserElo( '"' + str(arg1) + '"')

    winnerElo = list(winnerElo)
    winnerElo = ''.join(map(str, winnerElo))
    winnerElo = winnerElo.split("(")[1]
    winnerElo = winnerElo.split(",")[0]

    if (loserM != None):
        loserElo = await getUserElo( '"' + str(loserM.id) + '"')
    else:
        loserElo = await getUserElo( '"' + str(arg2) + '"')
        
    loserElo = list(loserElo)
    loserElo = ''.join(map(str, loserElo))
    loserElo = loserElo.split("(")[1]
    loserElo = loserElo.split(",")[0]
    
    winnerProb = await calculateWinnerProb(int(winnerElo), int(loserElo))
    newElos = await calculateNewELO(winnerProb, int(winnerElo), int(loserElo))
    
    if (loserM != None):
        await setUserElo(newElos[1], '"' + str(loserM.id) + '"')
    else:
        await setUserElo(newElos[1], '"' + str(arg2) + '"')
        
    if (winnerM != None):
        await setUserElo(newElos[0], '"' + str(winnerM.id) + '"')
    else:
        await setUserElo(newElos[0], '"' + str(arg1) + '"')


@bot.command(pass_context = True)
async def WhatsMyElo(ctx):
    print(ctx.message.author.id)
    try:
        elo = await getUserElo(str(ctx.message.author.id))
    except:
        elo = await getUserElo(str(ctx.message.author.name))
        
    elo = list(elo)
    elo = ''.join(map(str, elo))
    elo = elo.split("(")[1]
    print(elo)
    await ctx.message.channel.send("Your elo is " + elo.split(",")[0])

@bot.command(pass_context = True)
async def UpdateRank(ctx):
    global RoleList
    global RoleLocal
    member = ctx.message.author
    guild= ctx.guild
    try:
        link = await getLink('"' + str(member.id) + '"')
    except:
        link = await getLink('"' + str(member.name) + '"')
        
    print(link)
    
    rank = await checkRank(link)
    val = await checkRolesWithRank(rank, RoleLocal)

    for r in RoleList:
        try:
            role = discord.utils.get(guild.roles, r)
            await member.remove_roles(role)
        except:
            continue

    role = discord.utils.get(guild.roles, name=RoleList[val])
    await member.add_roles(role)

@bot.command(pass_context = True)
async def Commands(ctx):
    await ctx.message.channel.send("""```Commands:\n
r!Commands - Shows a list of all commands\n
r!SetupRoles - Adds the needed roles to the discord server (does not work with 2fa)\n
r!UpdateRank - Updates the message authors rank role\n
r!AddToDB DiscordPersonName scoresaber link (link can be Null) - adds a user to the database\n
r!UpdateAllRanks - Updates everyones rank role\n
r!WhatsMyElo - Tells the message author their ELO\n
r!UpdateElo winnername losername - Updates elo after 1v1s\n
r!EloLeaderboard - Outputs the elo leaderboard\n
r!RankLeaderboard - Outputs the scoresaber rank leaderboard for this server\n
```""")

@bot.command(pass_context=True)
@commands.has_role('Tourney Admins')
async def EloLeaderboard(ctx):
    await ctx.message.channel.send("Sorry not coded yet")


@bot.command(pass_context=True)
@commands.has_role('Tourney Admins')
async def RankLeaderboard(ctx):
    Headers = ["Server Rank", "Player Name", "Rank"]
    vals = await getAll()
    newList = []
    newDict = {}
    for i in list(vals):
        Rank = await checkRank(list(i)[1])
        newList.append(Rank)
        newDict[Rank] = i
        
    sortedList = await getSortedListBasedOnRank(newDict, newList)
    print(sortedList)
    newList2 = []
    for i in sortedList:
        newList2.append([ctx.guild.get_member(int(i[0])), await checkRank(list(i)[1])])
        
    List = await makeTable(newList2)
    HelpMe = Headers + List
    Table = await createTable(List, Headers)
    await ctx.message.channel.send(Table)
        
    

    
    


bot.run("Your token here")    


    
    
        

        
        
    
    


