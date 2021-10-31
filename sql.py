import sqlite3

connection = sqlite3.connect('RankBot.db')
cursor = connection.cursor()




#FUNCTIONS
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
async def getLinks():
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """SELECT Link FROM users;"""
    cursor.execute(command)
    output = cursor.fetchall()
    connection.commit()
    connection.close()

    return output

async def getLink(userID):
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """SELECT Link FROM users WHERE DiscordID = """ + userID + """;"""
    cursor.execute(command)
    output = cursor.fetchall()
    connection.commit()
    connection.close()

    return output


async def setLink(link, userID):
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """UPDATE users SET Link = """ + link + """ WHERE DiscordID = """ + userID + """; """
    cursor.execute(command)
    connection.commit()
    connection.close()

    

async def getAll():
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """SELECT * FROM users;"""
    cursor.execute(command)
    output = cursor.fetchall()
    connection.commit()
    connection.close()
    return output

async def getUserElo(userID):
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """SELECT ELO FROM users WHERE DiscordID = """ + userID + """; """
    cursor.execute(command)
    output = cursor.fetchall()
    connection.commit()
    connection.close()
    return output

async def setUserElo(elo, userID):
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """UPDATE users SET ELO = """ + str(elo) + """ WHERE DiscordID = """ + userID + """; """
    cursor.execute(command)
    connection.commit()
    connection.close()

async def addToDatabase(userID, link):
    connection = sqlite3.connect('RankBot.db')
    cursor = connection.cursor()
    command = """INSERT INTO users VALUES(""" + userID + """, """ + link + """, 1000);"""
    cursor.execute(command)
    connection.commit()
    connection.close()


    



