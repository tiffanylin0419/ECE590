from time import perf_counter
import collections
import sys
import functools

class TreeNode:
    def __init__(self, val, freq, left, right):
        self.val=val
        self.freq=freq
        self.left=left
        self.right=right
        self.cost = None
        pass
    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.val)
        left = str(self.left) if self.left is not None else '()'
        right = str(self.right) if self.right is not None else '()'
        return '({} {} {})'.format(self.val,left,right)
        
    def computeCost(self):
        if self.cost is not None:
            return self.cost
        def helper(n,depth):
            if n is None:
                return 0
            return depth * n.freq + helper(n.left, depth+1) + helper(n.right, depth +1)
        self.cost = helper(self, 1)
        return self.cost
    pass
pass

@functools.lru_cache(maxsize=500000)
def path(start,end,height):
    if end-start<0:
        return 0,0,None
    if start==end:
        #print(vals[start],freqs[start])
        return 0,height*freqs[start],TreeNode(vals[start],freqs[start],None, None)
    m_val=[]
    for i in range(start,end+1):
        l=path(start,i-1,height+1)
        r=path(i+1,end,height+1)
        m_val.append(l[1]+r[1]+height*freqs[i])
    mid_index=start+m_val.index(min(m_val))
    l=path(start,mid_index-1,height+1)
    r=path(mid_index+1,end,height+1)
    my_node=TreeNode(vals[mid_index],freqs[mid_index],l[2], r[2])
    #print(str(my_node))
    return mid_index,min(m_val),my_node



# Your code here.
if __name__ == "__main__":
    vals=[]
    freqs=[]
    with open(sys.argv[1]) as f:#
        for line in f.readlines():
            value,key=line.strip().split(':')
            vals.append(int(value))
            freqs.append(int(key))
    

    ans=path(0,len(vals)-1,1)#len(vals)-1
    print(ans[1])
    print(ans[2])
    
    times=[]
    for i in range(10):
        start = perf_counter()
        path(0,len(vals)-1,1)
        end = perf_counter()
        path.cache_clear()
        times.append(end-start)

    times.sort()
    time=times[(10+1)//2]
    print(int(time*pow(10,9)))





