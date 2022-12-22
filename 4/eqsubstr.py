# Write a function, which when iven one string (s) and two characters
# (c1 and c2), computes all pairings of contiguous ranges of c1s
# and c2s that have the same length.  Your function should return
# a set of three-tuples.  Each element of the set should be
# (c1 start index, c2 start index, length)
#
# Note that s may contain other characters besides c1 and c2.
# Example:
#  s = abcabbaacabaabbbb
#      01234567890111111  <- indices for ease of looking
#                1123456
#  c1 = a
#  c2 = b
#  Observe that there are the following contiguous ranges of 'a's (c1)
#  Length 1: starting at 0, 3, 9
#  Length 2: starting at 6, 11
#  And the following contiguous ranges of 'b's (c2)
#  Length 1: starting at 1, 10
#  Length 2: starting at 4
#  Length 4: starting at 13
#  So the answer would be
#  { (0, 1, 1), (0, 10, 1), (3, 1, 1), (3, 10, 1), (9, 1, 1), (9, 10, 1),
#    (6, 4, 2), (11, 4, 2)}
#  Note that the length 4 range of 'b's does not appear as there are no
#  Length 4 runs of 'a's.
from datetime import datetime
import random
import time
def printInt(data):
    for i in data:
        print("%7d" %i,",",sep="",end="")
    print()
def printFloat(data):
    for i in data:
        print("%2.5f" %i,",",sep="",end="")
    print()
    
def matching_length_sub_strs(s, c1, c2):
    dic1,dic2={},{}
    num1,num2=0,0
    i=0
    for i in range(len(s)):
        if s[i] == c1:
            num1+=1
            if num2!=0:
                if(num2 not in dic2):
                    dic2[num2]=[i-num2]
                else:
                    dic2[num2].append(i-num2)
                num2=0
        elif s[i] ==c2:
            if num1!=0:
                if(num1 not in dic1):
                    dic1[num1]=[i-num1]
                else:
                    dic1[num1].append(i-num1)
                num1=0
            num2+=1
        else:
            if num1!=0:
                if(num1 not in dic1):
                    dic1[num1]=[i-num1]
                else:
                    dic1[num1].append(i-num1)
                num1=0
            elif num2!=0:
                if(num2 not in dic2):
                    dic2[num2]=[i-num2]
                else:
                    dic2[num2].append(i-num2)
                num2=0
    if num1!=0:
        if(num1 not in dic1):
            dic1[num1]=[i-num1]
        else:
            dic1[num1].append(i-num1)
        num1=0
    elif num2!=0:
        if(num2 not in dic2):
            dic2[num2]=[i-num2]
        else:
            dic2[num2].append(i-num2)
        num2=0
    ans=set()
    for i in dic1:
        if i in dic2:
            for j in dic1[i]:
                for k in dic2[i]:
                    ans.add((j,k,i))
    return ans


# Makes a random string of length n
# The string is mostly comprised of 'a' and 'b'
# So you should use c1='a' and c2='b' when
# you use this with matching_length_sub_strs
def rndstr(n):
    def rndchr():
        x=random.randrange(7)
        if x==0:
            return chr(random.randrange(26)+ord('A'))
        if x<=3:
            return 'a'
        return 'b'
    ans=[rndchr() for i in range(n)]
    return "".join(ans)

def beststr(n):
    def rndchr():
        x=random.randrange(2)
        if x==0:
            return 'a'
        return 'b'
    return "".join([rndchr()]*n)

def worststr(n):
    x=random.randrange(2)
    ans=""
    if x==0:
        ans+="ab"*int(n/2)
        if n%2==1:
            ans+="a"
    else:
        ans+="ba"*int(n/2)
        if n%2==1:
            ans+="b"
    return ans
'''
def worststr(n):
    ans=""
    ans+="ab"*int(n/2)
    return ans'''

if __name__ == "__main__":
    ch1='a'
    ch2='b'
    
    size=512
    sizes=[]
    i=1
    while(i*size<= 16384):
        sizes.append(size*i)
        i*=2
    printInt(sizes)

    best=[]
    worst=[]
    rand=[]
    #best
    for sz in sizes:
        string=beststr(sz)
        start=datetime.now()
        ans=matching_length_sub_strs(string, ch1, ch2)
        best.append((datetime.now()-start).total_seconds())
    printFloat(best)

    #no use , only to make time calculation correct
    string=rndstr(sizes[0])
    start=datetime.now()
    ans=matching_length_sub_strs(string, ch1, ch2)
    t=(datetime.now()-start).total_seconds()
    #random
    for sz in sizes:
        string=rndstr(sz)
        start=datetime.now()
        ans=matching_length_sub_strs(string, ch1, ch2)
        rand.append((datetime.now()-start).total_seconds())
    printFloat(rand)
    
    #no use , only to make time calculation correct
    string=worststr(sizes[0])
    start=datetime.now()
    ans=matching_length_sub_strs(string, ch1, ch2)
    t=(datetime.now()-start).total_seconds()
    #worst
    for sz in sizes:
        string=worststr(sz)
        start=datetime.now()
        ans=matching_length_sub_strs(string, ch1, ch2)
        worst.append((datetime.now()-start).total_seconds())
    printFloat(worst)

