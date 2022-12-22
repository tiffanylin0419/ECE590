#Think of this Dfa class as being a "struct"
#with two fields:
# transitions = a 2D array representing the transition function
#   It gets index    transitions[statenum][input symbol]
# accepting = an array of booleans indicating which states are acceping
#   Index it with the statenumber.  Iff
#      acceping[statenum]
#   is true, then statenum is an accepting state.
# Note that the start state is always state 0
class Dfa:
    def __init__(self, transitions, accepting):
        self.transitions=transitions
        self.accepting=accepting
        pass
    pass


# A helper function that adds skipped state numbers.  
# If for some reason, our input skips a state number (e.g. specifies state 0, 2,3
# but not 1), this adds a the missing states with no transitions
# Note that transitions will get filled in to the "failstate" later.
def addSkippedStates(tmap, failstate):
    for i in range(0,failstate+1):
        if i not in tmap:
            tmap[i] = {}
            pass
        pass

# Anytime we dont specify a transition, we implicitly
# transition to a "fail state".  This function adds
# those mising transitions
def addFailTransitions(tmp, failstate):
    for state in tmp:
        tx=tmp[state]
        # We consider all ASCII characters [0,256)
        for i in range(0,256):
            # convert the number to the character
            c = chr(i)
            if c not in tx:
                tx[c] = failstate
                pass
            pass
        pass
    pass

# This is a helper which parses the transitions
# while reading the DFA.
# txinfo is a string with comma separate sym=state
# transition information, e.g. a=0,b=2,c=0,d=1
def parseTransitions(txinfo):
    m={}
    for inp in txinfo.split(","):
        inp=inp.strip()
        parts=inp.split("=")
        assert len(parts)==2, "Invalid input line: "^line^ " Need one equal in part "^inp
        m[parts[0]] = int(parts[1])
        pass
    return m

# This is a helper function for readDFA which does
# the actual file reading and parsing
def readDFAFile(fname):
    aset=set()
    tmap={}
    maxstate=0
    with open(fname) as f:
        for line in f:
            x=line.strip()
            # skip comments and blank lines
            if (x[0] =="#" or len(x)==0):
                continue
            # split state:transitions
            pieces=line.split(":")
            assert len(pieces) == 2, "Invalid input line: "^line^" expected exactly one :"
            if pieces[0] == "Accept":
                assert len(aset)==0, "Error: Multiple lines specifying accept states"
                aset={int(x) for x in pieces[1].split(",")}
                pass
            else:
                state=int(pieces[0])
                tmap[state] = parseTransitions(pieces[1])
                maxstate=max(state,maxstate)
                pass
            pass
        return (maxstate, aset, tmap)

# This function takes a filename and read
# a DFA from the file. It returns a Dfa object
def readDFA(fname):
    (maxstate, aset, tmap) = readDFAFile(fname)
    failstate=maxstate+1
    accepting=[i in aset for i in range(0,failstate+1)]
    addSkippedStates(tmap,failstate)
    addFailTransitions(tmap, failstate)
    transitions=[[tmap[i][chr(j)] for j in range(0,256)] for i in range(0, failstate+1)]
    return Dfa(transitions, accepting)


# You should write this function.
# It takes dfa (a Dfa object, as returned by readDFA)
# and s (a string)
# This function should start in state 0 of the dfa,
# process the string, and return true (if the DFA accepts)
# or false (if not)
def doDFA(dfa, s):
    # Replace this with your code
    s_len=len(s)
    node_num=0
    for i in range(s_len):
        node_num=dfa.transitions[node_num][ord(s[i])]
        if(node_num==len(dfa.transitions)-1):
            return False
    return dfa.accepting[node_num]

# quick example of how to use it
if __name__ == "__main__":
    def testDfa(name, dfa, s, expected):
        x=doDFA(dfa,s)
        if(x==expected):
            print(name +" gave "+ str(x)+ " as expected on " + s)
        else:
            print("****"+ name +" gave "+ str(x)+ " on " + s + " but expected " + str(expected))
            pass
        pass
    d1 = readDFA("odd1s.dfa")
    testDfa("odd1s", d1, "", False)
    testDfa("odd1s", d1, "0", False)
    testDfa("odd1s", d1, "1", True)
    testDfa("odd1s", d1, "10000101001010110", True)
    d2 = readDFA("mod3is2.dfa")
    testDfa("mod3is2", d2, "123456", False)
    testDfa("mod3is2", d2, "22245554888", True)
            
    pass
