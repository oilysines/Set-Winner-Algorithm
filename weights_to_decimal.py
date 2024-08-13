import math
while True:
    l = input('').replace('[','').replace(']','').split(',')
    l = [eval(i) for i in l]
    s= sum(l)
    total = 0
    for i in l:
        n = i/s
        print(round(n,2))
        total += round(n,2)
    print('Total:',total)
        
