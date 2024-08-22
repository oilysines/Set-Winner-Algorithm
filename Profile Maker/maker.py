import requests
import datetime
import re
import os
import csv
import json

path = os.getcwd()
minusone = os.path.dirname(path)
stagelist = []

#extracting stagelist data
stage_txt = open(r'%s/Stagelist.txt' % path)

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

# name
print("What is this player's tag? (pay attention to case)")
name = input('')
if name == 'This is gonna sound crazy but... Are you my dad?':
    print('Hi Gorgug')
    input('')
    exit('')
print('')
# Player-Stage Data
print(f"Rank all these stages from best to worst for {name}.")
print('(The stages should be acronyms in a list separated by commas)')
print('ex. BF, FD, PS2, etc.')
print('Select from the following Stages:')

def give_acronym(st):
    acronyms = open(r'%s\acronyms.csv' % path)
    acro = csv.reader(acronyms)
    for line in acro:
        if st == line[0]:
            acronyms.close()
            return line[1],line[0]
        else:
            pass
    acronyms.close()

starter_abb = []
for stage in stagelist:
    corr = give_acronym(stage)
    print(corr[0]+" - "+corr[1].replace(r'Ã©',r'é'))

stagerank = []
listed_rank = input('')
stagerank_raw = re.findall(r'[^,\s\n\(\)\[\]]+',listed_rank)
stagerank = []
#print(stagerank_raw)
for s in stagerank_raw:
    #print('\n',s)
    for stage in starters:
        #print(stage)
        acro = give_acronym(stage)[0]
        #print(s.lower(),acro.lower())
        if s.lower() == acro.lower():
            starter_abb.append(acro)
            stagerank.append(acro) 
            break
    for stage in counterpicks:
        acro = give_acronym(stage)[0]
        #print(s.lower(),acro.lower())
        if s.lower() == acro.lower():
            stagerank.append(acro)
            break
            
#print(starter_abb)
#print(stagerank)

#Closer/Choker
print('')
print(f'Is {name} a Closer or a Choker?')
print('Closers are more likely to win evenly matched games,\nas well as being more likely to win sets 3-0.')
print('Chokers are more likely to have very close sets and tend to have worse consistency')
print('0 - Closer\n1 - Choker')
pt_respond = input('')
if pt_respond == '0':
    p_type = 'Closer'
elif pt_respond == '1':
    p_type = 'Choker'
else:
    print('invalid response given: automatically setting to choker')
    p_type = 'Choker'

print('')

#Writing the Payload
playerdict = {
    "Starter Ranking": starter_abb,
    "Stage Ranking": stagerank,
    "Player Type": p_type,
}
payload = json.dumps(playerdict,indent=4)
with open(r'%s\Outputs\%s.json' % (path, name),"w") as outfile:
    outfile.write(payload)
print('Payload successfully written')
input('Press ENTER to exit')
