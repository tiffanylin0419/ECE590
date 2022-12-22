from time import perf_counter
import sys
import functools
sys.setrecursionlimit(2000)

@functools.lru_cache(maxsize=2000)
def path(i,j):
    if i==h-1 and j==w-1:
        return grid[i][j]
    if i==h-1:
        directions[i][j]=0#West?
        return grid[i][j]+path(i,j+1)
    if j==w-1:
        directions[i][j]=1
        return grid[i][j]+path(i+1,j)
    N=path(i+1,j)
    W=path(i,j+1)
    if N>W:
        directions[i][j]=1
        return grid[i][j]+N
    else:
        directions[i][j]=0
        return grid[i][j]+W


def printDir(direction):
    for i in range(len(direction)-1,-1,-1):
        if direction[i]==1:
            print("N",end="")
        else:
            print("W",end="")
    print()

def getDir(aa):
    direction=[]
    i,j=0,0
    while aa[i][j]!=-1 and i<h and j<w:
        if aa[i][j]==1:
            i+=1
            direction.append(1)
        else:
            j+=1
            direction.append(0)
    return direction

if __name__ == "__main__":
    grid=[]
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            grid.append([int(x) for x in line.strip().split(',')])
    h=len(grid)
    w=len(grid[0])
    directions=[[-1]*w for i in range(h)]

   
    times=[]
    for i in range(10):
        start = perf_counter()
        coin=path(0,0)
        end = perf_counter()
        times.append(end-start)
        #print(path.cache_info())
        path.cache_clear()
        #print(path.cache_info())

    times.sort()
    time=times[(10+1)//2]

    direction=getDir(directions)
    
    printDir(direction)
    print(coin)
    print(int(time*pow(10,9)))
    
