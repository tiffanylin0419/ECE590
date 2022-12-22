# removes duplicates from data.
# This function keeps the last occurence of each element
# and preserves order.
# So rmdup([1,2,3,2,1,4,2]) should return [3,1,4,2]
from datetime import datetime
import random


def genArr(size,num):
    data=[]
    for i in range(size):
        data.append(random.randrange(0,num))
    return data

def printInt(data):
    for i in data:
        print("%7d" %i,",",sep="",end="")
    print()
def printFloat(data):
    for i in data:
        print("%2.5f" %i,",",sep="",end="")
    print()
    
def reverse(data):
    for i in range(int(len(data)/2)):
        data[i],data[len(data)-1-i]=data[len(data)-1-i],data[i]
    return data

def rmdup(data,num):
    ans_rev=[]
    position_empty=[True]*num
    for i in range(len(data)-1,-1,-1):
        if position_empty[data[i]]:
            ans_rev.append(data[i])
        else:
            position_empty[data[i]]=False
    ans=reverse(ans_rev)
    return ans

if __name__ == "__main__":
    size=4096
    sizes=[]
    i=1
    while(i*size<= 4194304):
        sizes.append(size*i)
        i*=2
    printInt(sizes)
        
    many=[]
    moderate=[]
    rare=[]
    #many
    for sz in sizes:
        num=int(sz/2048)
        data_many=genArr(sz,num)
        start=datetime.now()
        ans=rmdup(data_many,num)
        many.append((datetime.now()-start).total_seconds())
    printFloat(many)

    #no use
    sz=sizes[0]
    num=int(sz/16)
    data_moderate=genArr(sz,num)
    start=datetime.now()
    ans=rmdup(data_moderate,num)
    t=(datetime.now()-start).total_seconds()
    #moderate
    for sz in sizes:
        num=int(sz/16)
        data_moderate=genArr(sz,num)
        start=datetime.now()
        ans=rmdup(data_moderate,num)
        moderate.append((datetime.now()-start).total_seconds())
    printFloat(moderate)

    #no use
    sz=sizes[0]
    num=sz*4
    data_rare=genArr(sz,num)
    start=datetime.now()
    ans=rmdup(data_rare,num)
    t=(datetime.now()-start).total_seconds()
    #rare
    for sz in sizes:
        num=sz*4
        data_rare=genArr(sz,num)
        start=datetime.now()
        ans=rmdup(data_rare,num)
        rare.append((datetime.now()-start).total_seconds())
    printFloat(rare)
