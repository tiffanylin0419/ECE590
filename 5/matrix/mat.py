from time import perf_counter
import sys
import functools
sys.setrecursionlimit(500000)

@functools.lru_cache(maxsize=500000)
def path(start,end):
    if end-start==1:
        return size[start]*size[end]*size[end+1],(name[start],name[end])
    m=[i for i in range(start,end)]
    m_val=[]
    for i in m:
        if i==start:
            m_val.append(path(i+1,end)[0]+size[start]*size[i+1]*size[end+1])
        elif i==end-1:
            m_val.append(path(start,i)[0]+size[start]*size[i+1]*size[end+1])
        else:    
            m_val.append(path(start,i)[0]+path(i+1,end)[0]+size[start]*size[i+1]*size[end+1])
    
    mid_index=m_val.index(min(m_val))
    if m[mid_index]==start:
        return (min(m_val)),(name[start],path(m[mid_index]+1,end)[1])
    elif m[mid_index]==end-1:
        return (min(m_val)),(path(start,m[mid_index])[1],name[end])
    return min(m_val),(path(start,m[mid_index])[1],path(m[mid_index]+1,end)[1])
    
    
if __name__ == "__main__":
    grid=[]
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            grid.append([x for x in line.strip().split(',')])

    name=[x[0] for x in grid]
    size=[int(grid[0][1])]
    size+=[int(x[2]) for x in grid]
    l=len(name)

    s,operations=path(0,l-1)
    print(operations)
    print(s)
    

    times=[]
    for i in range(10):
        start = perf_counter()
        path(0,l-1)
        end = perf_counter()
        times.append(end-start)
        #print(path.cache_info())
        path.cache_clear()
        #print(path.cache_info())

    times.sort()
    time=times[(10+1)//2]
    print(int(time*pow(10,9)))
    
