# This function takes 2 matricies (as lists of lists)
# and performs matrix multiplication on them.
# Note: you may not use any matrix multiplication libraries.
# You need to do the multiplication yourself.
# For example, if you have
#     a=[[1,2,3],
#        [4,5,6],
#        [7,8,9],
#        [4,0,7]]
#     b=[[1,2],
#        [3,4],
#        [5,6]]
#  Then a has 4 rows and 3 columns.
#  b has 3 rows and 2 columns.
#  Multiplying a * b results in a 4 row, 2 column matrix:
#  [[22, 28],
#   [49, 64],
#   [76, 100],
#   [39, 50]]
from datetime import datetime
import random

def genArr(size1,size2):
    datas=[]
    data=[]
    for i in range(size1):
        for j in range(size2):
            data.append(random.randrange(0,10))
        datas.append(data)
        data=[]
    return datas

def printInt(data):
    for i in data:
        print("%7d" %i,",",sep="",end="")
    print()
def printFloat(data):
    for i in data:
        print("%2.5f" %i,",",sep="",end="")
    print()
    
def matrix_mul(a,b):
    # Write me
    assert(len(a[0])==len(b))
    c= [[0]*len(b[0]) for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                c[i][j]+=a[i][k]*b[k][j]      
    return c



if __name__ == "__main__":
    size=4
    sizes=[]
    i=1
    while(i*size<= 512):
        sizes.append(size*i)
        i*=2
    printInt(sizes)
    
    many=[]
    square=[]
    few=[]
    #many
    for sz in sizes: 
        a=genArr(4*sz,sz)
        b=genArr(sz,int(sz/4))
        start=datetime.now()
        c=matrix_mul(a,b)
        many.append((datetime.now()-start).total_seconds())
    printFloat(many)

    #no use
    a=genArr(sizes[0],sizes[0])
    b=genArr(sizes[0],sizes[0])
    start=datetime.now()
    c=matrix_mul(a,b)
    t=(datetime.now()-start).total_seconds()
        
    #square
    for sz in sizes:
        a=genArr(sz,sz)
        b=genArr(sz,sz)
        start=datetime.now()
        c=matrix_mul(a,b)
        square.append((datetime.now()-start).total_seconds())
    printFloat(square)

    #no use
    a=genArr(4*sizes[0],sizes[0])
    b=genArr(sizes[0],int(sizes[0]/4))
    start=datetime.now()
    c=matrix_mul(a,b)
    t=(datetime.now()-start).total_seconds()
    
    #few
    for sz in sizes:
        a=genArr(4*sz,sz)
        b=genArr(sz,int(sz/4))
        start=datetime.now()
        c=matrix_mul(a,b)
        few.append((datetime.now()-start).total_seconds())
    printFloat(few)
