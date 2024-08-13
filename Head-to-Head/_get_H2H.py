import os
import requests
import json
import datetime

path = os.getcwd()

print(datetime.datetime.now())

#credentials
with open(r'%s\credentials.json' % path) as cred:
    data = json.load(cred)
    sheet_id = data['Link']
    API_Key = data['API KEY']
    cred.close()

H2HData = []
GET = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/H2HData!A2:E?key={API_Key}')
json = GET.json()
for _set in json['values']:
        H2HData.append(_set)

print(H2HData)

playerlist = []
setwl = []
gamewl = []
for pair in H2HData:
    if pair[0] not in playerlist:
        playerlist.append(pair[0])
    if pair[2] not in playerlist:
        playerlist.append(pair[2])

#set H2H
for p1 in playerlist:
    for p2 in playerlist:
        wins = 0
        losses = 0
        for pair in H2HData:
            if pair[0] == p1 and pair[2] == p2:
                wins += 1
            if pair[0] == p2 and pair[2] == p1:
                losses += 1
        if wins == 0 and losses == 0:
            pass
        else:
            appendage = f'{p1},{wins},{losses},{p2}'
            setwl.append(appendage)
            print(appendage)
print('')
#game H2H
for p1 in playerlist:
    for p2 in playerlist:
        wins = 0
        losses = 0
        for pair in H2HData:
            if pair[0] == p1 and pair[2] == p2:
                wins += int(pair[1])
                losses += int(pair[3])
            if pair[0] == p2 and pair[2] == p1:
                losses += int(pair[1])
                wins += int(pair[3])
        if wins == 0 and losses == 0:
            pass
        else:
            appendage = f'{p1},{wins},{losses},{p2}'
            gamewl.append(appendage)
            print(appendage)

print('\nData retrieval successful.')
print('Which would you like to save?')
print('0 - sets\n1 - games\n2 - both')

def setWrite():
    #set write
    with open('setData.csv', 'w') as sD:
        sD.write(str(datetime.datetime.now())+'\n')
        for s in setwl:
            if setwl.index(s) == len(setwl)-1:
                sD.write(s)
            else:
                sD.write(s+'\n')

def gameWrite():
    #game write
    with open('gameData.csv', 'w') as gD:
        gD.write(str(datetime.datetime.now())+'\n')
        for g in gamewl:
            if gamewl.index(g) == len(gamewl)-1:
                gD.write(g)
            else:
                gD.write(g+'\n')

while True:
    savevar = input('')
    if savevar == '0':
        setWrite()
        break
    elif savevar == '1':
        gameWrite()
        break
    elif savevar == '2':
        setWrite()
        gameWrite()
        break
    else:
        print('INVALID RESPONSE, please try again')
                
