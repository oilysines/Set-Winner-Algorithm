import os
import time
import json
import random, numpy
import csv
import re

path = os.getcwd()

sts = 0.032
wrstep = 0.065
nrstep = 0.05

bp = 100
playerlist = []
qlist = ['Player 1','Player 2','Set Record', 'Game Record']
#get players
for j in os.listdir(r'%s\Profile Maker\Outputs' % path):
    p = j.replace('.json','')
    playerlist.append(p)

#extracting stagelist data
def get_acro_data(st):
    acronyms = open(r'%s\Profile Maker\acronyms.csv' % path)
    acro = csv.reader(acronyms)
    for line in acro:
        if st == line[0] or st == line[1]:
            acronyms.close()
            return line[1], line[0]
        else:
            pass
    acronyms.close()

stage_txt = open(r'%s\Profile Maker\Stagelist.txt' % path)

starters = []
counterpicks = []

stagefix = ','.join(stage_txt)

try:
    starter1 = re.findall(r'(?<=Starters:\W)[\s\S]+(?=\W\WCounterpicks:)',stagefix)[0]
except:
    print('no starter data')
    starter1 = ''
try:
    counterpick1 = re.findall(r'(?<=Counterpicks:\W)[\s\S]+(?=\W\W,DSR:)',stagefix)[0]
except:
    print('no counterpick data')
    counterpick1 = ''

starter1 = starter1.replace(r',','')
counterpick1 = counterpick1.replace(r',','')

starters = starter1.split('\n')
starters = list(filter(None, starters))
#print(starters)
counterpicks = counterpick1.split('\n')
counterpicks = list(filter(None,counterpicks))
#print(counterpicks)

stagelist = starters + counterpicks

starter_abb = []
counter_abb = []
for stage in starters:
    starter_abb.append(get_acro_data(stage)[0])
for stage in counterpicks:
    counter_abb.append(get_acro_data(stage)[0])

stagelist_abb = starter_abb + counter_abb

#print(starter_abb)
#print(counter_abb)

#player select 1
print('Player 1:')
avp = list(playerlist)
for p in avp:
    index = avp.index(p)
    print(f'{index} - {p}')
while True:
    p1i = input('')
    #p1i = 0
    if int(p1i) not in range(0,len(avp)):
        print('INVALID RESPONSE, please try again')
    else:
        break

p1 = avp[int(p1i)]
with open(r'%s\Profile Maker\Outputs\%s.json' % (path,p1)) as p1profile:
    p1json = json.load(p1profile)
    p1starters = p1json['Starter Ranking']
    p1stages = p1json['Stage Ranking']
    p1type = p1json['Player Type']

#player select 2
avp.pop(int(p1i))
print('')
print('Player 2:')
for p in avp:
    index = avp.index(p)
    print(f'{index} - {p}')
while True:
    p2i = input('')
    #p2i = '1'
    if int(p2i) not in range(0,len(avp)):
        print('INVALID RESPONSE, please try again')
    else:
        break

p2 = avp[int(p2i)]
with open(r'%s\Profile Maker\Outputs\%s.json' % (path,p2)) as p2profile:
    p2json = json.load(p2profile)
    p2starters = p2json['Starter Ranking']
    p2stages = p2json['Stage Ranking']
    p2type = p2json['Player Type']

print(f'{p1} vs. {p2}')
#get records
print('\nFetching records...')
time.sleep(0.20)
print('...')
time.sleep(0.15)
def setRecord():
    with open(r'%s\Head-to-Head\setData.csv' % path,'r+') as sD:
        sDr = csv.reader(sD)
        next(sDr)
        for line in sDr:
            #print(line)
            if line[0] == p1 and line[3] == p2:
                return line
        return p1,'0','0',p2

def gameRecord():
    with open(r'%s\Head-to-Head\gameData.csv' % path,'r+') as gD:
        gDr = csv.reader(gD)
        next(gDr)
        for line in gDr:
            #print(line)
            if line[0] == p1 and line[3] == p2:
                return line
        return p1,'0','0',p2

#record number stuff
sR = setRecord()
gR = gameRecord()
print(sR[0],sR[1]+'-'+sR[2],sR[3])
print(gR[0],gR[1]+'-'+gR[2],gR[3])

if sR[1] == '0' and sR[2] == '0':
    sWR = 1
    gWR = 1
else:
    sWR = int(sR[1])/(int(sR[2])+int(sR[1]))
    gWR = int(gR[1])/(int(gR[2])+int(gR[1]))
    #print(sWR)
    #print(gWR)

p1WMs = 0.6*sWR+0.7

p1WMg = 0.6*gWR+0.7

p1WM = p1WMs * p1WMg
#print(p1WM)

#neutral and punish
print("\nDescribe the players' neutral as a ratio (P1:P2)")
print('ex. 50:50 (meaning that both players win neutral the same amount on average')
while True:
    inrat = input('')
    #inrat = '1:1'
    #print(inrat)
    if ':' not in inrat:
        print('INVALID RESPONSE, please try again')
    else:
        ratspl = inrat.split(':')
        #print(ratspl)
        break

ratvar = int(ratspl[0])/(int(ratspl[0])+int(ratspl[1]))
#print(ratvar)
NRMp1 = 0.6*ratvar+0.7
#print(NRMp1)
#print(NRMp2)

print(f"\nOn a scale from 0 to 10 (can have decimals),\nHow strong is {p1}'s punish game in this matchup?")
while True:
    try:
        p1P = float(input(''))
        #p1P = 5
        #print(p1P)
    except:
        pass
    if p1P < 0 or p1P > 10:
        print('INVALID RESPONSE, please try again')
    else:
        break

print(f"\nOn a scale from 0 to 10 (can have decimals),\nHow strong is {p2}'s punish game in this matchup?")
while True:
    try:
        p2P = float(input(''))
        #p2P = 5
        #print(p2P)
    except:
        pass
    if p2P < 0 or p2P > 10:
        print('INVALID RESPONSE, please try again')
    else:
        break

p1PM = 0.687+p1P**1.28/25
p2PM = 0.687+p2P**1.28/25

#Gameplay variable
p1GV = round(p1WM*NRMp1*p1PM,3)
p2GV = round(p2PM,3)
#print(p1PM,p2PM)
#print(p1GV,p2GV)

#arranging games
print('\nAre you doing a single game or a set?')
print('0 - Single game\n1 - Set')
while True:
    try:
        mt = int(input(''))
        #mt = 1
        #print(mt)
    except:
        pass
    if mt == 0:
        print('Which game of the set is this')
        print('ex. 1/3 (for game 1 in a best of 3)')
        while True:
            sgr = input('')
            #sgr = '2/3'
            #print(sgr)
            if '/' not in sgr:
                print('a / was missing from your response')
            else:
                sgr = sgr.split('/')
                if sgr[1] not in ['3','5']:
                    print('Invalid game total, please try again')
                elif sgr[0] > sgr[1]:
                    print('Invalid game number, please try again')
                else:
                    game = int(sgr[0])-1
                    winvar = round(0.667*int(sgr[1]),0)
                    break
        
        print('\nWhich stage?')
        if game == 0:
            for stage in starters:
                print(starters.index(stage),'-',stage)
        else:
            for stage in stagelist:
                print(stagelist.index(stage),'-',stage)
        while True:
            try:
                gamestage_index = int(input(''))
                #gamestage_index = 6
                #print(gamestage_index)
                if game == 0:
                    if 0 <= gamestage_index <= len(starters)-1:
                        break
                    else:
                        print('INVALID RESPONSE, please try again')
                elif game > 0:
                    if 0 <= gamestage_index <= len(stagelist)-1:
                        break
                    else:
                        print('INVALID RESPONSE, please try again')
                else:
                    print('INVALID RESPONSE, please try again')
            except:
                print('INVALID RESPONSE, please try again')
        if game == 0:
            if 0 <= gamestage_index <= len(starters)-1:
                gamestage = get_acro_data(starters[gamestage_index])[0].replace('Ã©','é')
                break
            else:
                print('INVALID RESPONSE, please try again')
        elif 1 <= game <= 4:
            if 1 <= gamestage_index <= len(stagelist)-1:
                gamestage = get_acro_data(stagelist[gamestage_index])[0].replace('Ã©','é')
                break
            else:
                print('INVALID RESPONSE, please try again')
    elif mt == 1:
        print('\nbo3 or bo5?')
        print('0 - bo3\n1 - bo5')
        while True:
            winput = input('')
            #winput = '1'
            #print(winput)
            if winput not in ['0','1']:
                print('INVALID RESPONSE, please try again')
            elif winput == '0':
                game = 0
                winvar = 2
                break
            elif winput == '1':
                game = 0
                winvar = 3
                break
        break
    else:
        pass

#Closer and Choker modifiers
bo3_Closer = [1,1.075,1.15]
bo5_Closer = [1,1.03,1.06,1.09,1.12,1.15]

bo3_Choker = [1.15,1.075,1]
bo5_Choker = [1.15,1.12,1.09,1.06,1.03,1]

if winvar == 2:
    p1PlayList = 'bo3_'+p1type
    p2PlayList = 'bo3_'+p2type
elif winvar == 3:
    p1PlayList = 'bo5_'+p1type
    p2PlayList = 'bo5_'+p2type

def coinflip():
    global flip, ep1, ep2, ep1_name, ep2_name
    flip = random.randint(0,1)
    if flip == 0:
        print(f'\n{p1} won the coinflip')
        ep1 = 'p1'
        ep2 = 'p2'
        ep1_name = p1
        ep2_name = p2
    else:
        print(f'\n{p2} won the coinflip')
        ep1 = 'p2'
        ep2 = 'p1'
        ep1_name = p2
        ep2_name = p1

#Stage Modifiers
p1_stagemods = {}
p2_stagemods = {}
for i in range(0,len(stagelist)):
    p1_stagemods[f'{p1stages[i]}'] = round((1+4*sts)-i*sts,3)
    p2_stagemods[f'{p2stages[i]}'] = round((1+4*sts)-i*sts,3)

#Stage Select
def stage_select(g):
    global gamestage
    #currently this wont have ban patterns or strikestepping bc im BOREDDDDD
    #so this just assumes you have 5 starters :p
    if g == 0:
        strikelist = list(starter_abb)
        print('\nStarters:')
        print(*strikelist,sep='\n')

        time.sleep(0.5)
        ep1_worst2_1_1 =  globals()[f'{ep1}starters'][-2:]
        ep1_firststrike = numpy.random.choice(ep1_worst2_1_1,size=1,replace=False)[0]
        strikelist.remove(ep1_firststrike)
        globals()[f'{ep1}starters'].remove(ep1_firststrike)
        globals()[f'{ep2}starters'].remove(ep1_firststrike)
        print(f'\n{ep1_name} bans {ep1_firststrike}') 

        time.sleep(0.5)
        ep2_worst4_1 = globals()[f'{ep2}starters'][-3:]
        ep2_doublestrike = numpy.random.choice(ep2_worst4_1,size=2,replace=False,p=[0.22,0.39,0.39])
        for stage in ep2_doublestrike:
            strikelist.remove(stage)
            globals()[f'{ep1}starters'].remove(stage)
            globals()[f'{ep2}starters'].remove(stage)
        print(f'{ep2_name} bans {ep2_doublestrike[0]} and {ep2_doublestrike[1]}')

        time.sleep(0.5)
        ep1_finalstrike = globals()[f'{ep1}starters'][-1]
        strikelist.remove(ep1_finalstrike)
        gamestage = strikelist[0]
        print(f'{ep1_name} bans {ep1_finalstrike}')
        time.sleep(0.5)
        print('\nGame 1: '+get_acro_data(gamestage)[1])
        
    elif g == 1:
        strikelist = list(stagelist_abb)
        print('\nStages:')
        print(*strikelist,sep='\n')
        ep1_stages_2 = list(globals()[f'{lastwinner}stages'])
        ep2_stages_2 = list(globals()[f'{lastloser}stages'])
        time.sleep(0.5)
        
        ep1_worst4_2 = ep1_stages_2[-4:]
        ep1_ds_2 = numpy.random.choice(ep1_worst4_2,size=2,replace=False,p=[0.18,0.22,0.3,0.3])
        for stage in ep1_ds_2:
            strikelist.remove(stage)
            ep1_stages_2.remove(stage)
            ep2_stages_2.remove(stage)
        print('\n'+globals()[f'{lastwinner}']+f' bans {ep1_ds_2[0]} and {ep1_ds_2[1]}')
        time.sleep(0.5)

        ep2_best_3_2 = ep2_stages_2[:3]
        ep2_choice_2_2 = numpy.random.choice(ep2_best_3_2,size=1,replace=False,p=[0.43,0.35,0.22])[0]
        print(globals()[f'{lastloser}']+f' chooses {ep2_choice_2_2}')
        gamestage = ep2_choice_2_2
        time.sleep(0.5)
        
    elif g >= 2:
        strikelist = list(stagelist_abb)
        print('\nStages:')
        print(*strikelist,sep='\n')
        ep1_stages_3 = list(globals()[f'{lastwinner}stages'])
        ep2_stages_3 = list(globals()[f'{lastloser}stages'])
        for stage in globals()[f'{lastwinner}DSR']:
            try:
                ep1_stages_3.remove(stage)
            except:
                pass
        for stage in globals()[f'{lastloser}DSR']:
            try:
                ep2_stages_3.remove(stage)
            except:
                pass
        #print(globals()[f'e{lastwinner}_name'],ep1_stages_3)
        #print(globals()[f'e{lastloser}_name'],ep2_stages_3)
            time.sleep(0.5)

        ep1_worst4_3 = ep1_stages_3[-4:]
        ep1_ds_3 = numpy.random.choice(ep1_worst4_3,size=2,replace=False,p=[0.18,0.22,0.3,0.3])
        for stage in ep1_ds_3:
            strikelist.remove(stage)
            try:
                ep1_stages_3.remove(stage)
            except:
                pass
            try:
                ep2_stages_3.remove(stage)
            except:
                pass
        print('\n'+globals()[f'{lastwinner}']+f' bans {ep1_ds_3[0]} and {ep1_ds_3[1]}')
        time.sleep(0.5)

        ep2_best_3_3 = ep2_stages_3[:3]
        ep2_choice_2_3 = numpy.random.choice(ep2_best_3_3,size=1,replace=False,p=[0.5,0.38,0.12])[0]
        print(globals()[f'{lastloser}']+f' chooses {ep2_choice_2_3}')
        gamestage = ep2_choice_2_3
        time.sleep(0.5)

#Simulator
p1DSR = []
p2DSR = []
def simulate(game,stage):
    global p1DSR,p2DSR,p1score,p2score
    global lastwinner,lastloser,ep1_name,ep2_name
    #print(f'{p1}:',str(p1_stagemods[stage])+'x')
    #print(f'{p2}:',str(p2_stagemods[stage])+'x')
    p1_points = bp * p1GV * p1_stagemods[stage] * eval(p1PlayList)[game]
    p2_points = bp * p2GV * p2_stagemods[stage] * eval(p2PlayList)[game]
    #print(f'{bp} * {p1GV} * {p1_stagemods[stage]} * {eval(p1PlayList)[game]}')
    #print(f'{bp} * {p2GV} * {p2_stagemods[stage]} * {eval(p2PlayList)[game]}')    
    p1_points_percent = round(100*(p1_points/(p1_points+p2_points)))
    p2_points_percent = 100-p1_points_percent
    print(f'\nOn a 1-{p1_points_percent}, {p1} Wins')
    print(f'On a {p1_points_percent+1}-100, {p2} Wins')
    input('Press ENTER to roll the metaphorical dice')
    result = random.randint(1,100)
    print(result)
    if result <= p1_points_percent:
        print(f'{p1} Wins!')
        p1DSR.append(stage)
        #print(p1,p1DSR)
        lastwinner = 'p1'
        lastloser = 'p2'
        p1score += 1
    else:
        print(f'{p2} Wins!')
        p2DSR.append(stage)
        #print(p2,p2DSR)
        lastwinner = 'p2'
        lastloser = 'p1'
        p2score += 1

p1score = 0
p2score = 0
if mt == 0:
    simulate(game,gamestage)
elif mt == 1:
    coinflip()
    while True:
        if p1score < winvar and p2score < winvar:
            stage_select(game)
            simulate(game,gamestage)
            game += 1
            time.sleep(1)
        else:
            break
    if p1score > p2score:
        print(f'\n{p1} wins the set {p1score}-{p2score}!')
    else:
        print(f'\n{p2} wins the set {p2score}-{p1score}!')

input('Press ENTER twice to exit')
input('')
