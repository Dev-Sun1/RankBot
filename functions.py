import requests
from bs4 import BeautifulSoup

async def checkIfUserIsInDB(List, link):
    found = False

    if link == "Null":
        found = True
    else:
        for i in List:
            if i == link:
                print("There is already a user in this database with that link")
                found = True
    return found

async def calculateNewELO(winnerProb, winnerELO, loserELO):
    wElo = winnerELO + (32 * (1 - winnerProb))
    lElo = loserELO + (32 * (0 - (1 - winnerProb)))
    return [wElo, lElo]
    

async def checkRank(link):
    link = list(link)
    link = ''.join(map(str, link))
    if link == "Null":
        return(link)
    else:
        try:
            link = link.split("'")[1]
        except:
            a = 2
            
        req = requests.get(link)
        html_page = req.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        rank = 999999
        for t in text:
            if t.startswith('#'):
                rank = t

        rank = rank.split('#')[1]
        rank = str(rank)
        try:
            rank = rank.split(",")[0] + rank.split(",")[1]
        except:
            a = 1

        return int(rank)       
        
async def checkRolesWithRank(rank, Roles):
    val = 0
    done = False
    if(rank == "Null"):
        return rank
    while not done:
        if int(rank) <= int(Roles[val]):
            done = True
        else:
            val += 1

        if val > len(Roles) - 1:
            done = True
            
    return val

async def calculateWinnerProb(winnerELO, loserELO):
    winnerProb = 1 / 1 - 10**((winnerELO - loserELO)/400)
    return winnerProb

async def makeTable(values):
    List = []
    for i in values:
        try:
            List.append([list(i)[0].name, list(i)[1]])
        except:
            continue
    
    return List

async def getSortedListBasedOnRank(vals, ranks):
    List = []
    temp = {}
    intVals = []
    run = True
    
    counter = 0
    for key, value in vals.items():
        if not isinstance(key, str):
            temp[key] = value

    keys = list(temp.keys())
    sortedKeys = sorted(keys)
    print(sortedKeys)
    for i in sortedKeys:
        List.append(temp[i])
        
        
            
    print(List)
    return List
    


