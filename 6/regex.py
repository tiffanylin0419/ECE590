from nfa import *
from state import *
import string
class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        front=self.children[0].transformToNFA()
        back=self.children[1].transformToNFA()
        len1=len(front.states)
        front.addStatesFrom(back)
        for i in range(len1):
            if front.is_accepting[i]:
                front.addTransition(front.states[i],front.states[len1])
        for i in range(len1):
            front.is_accepting[i]=False
        for i in back.alphabet:
            if i not in front.alphabet:
                front.alphabet.append(i)    
        return front
        
        pass
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        front=self.children[0].transformToNFA()
        len1=len(front.states)
        for i in range(1,len1):
            if front.is_accepting[i]:
                front.addTransition(front.states[i],front.states[0])
        front.is_accepting[0]=True
        return front
        pass
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        front=self.children[0].transformToNFA()
        back=self.children[1].transformToNFA()
        len1=len(front.states)
        front.addStatesFrom(back)
        front.addTransition(front.states[0],front.states[len1])
        for i in back.alphabet:
            if i not in front.alphabet:
                front.alphabet.append(i)
        return front
        pass
    pass

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        nfa=NFA()
        nfa.states=[State(0),State(1)]
        nfa.states[0].transition[self.sym]=[nfa.states[1]]
        nfa.is_accepting[0]=False
        nfa.is_accepting[1]=True
        if self.sym not in nfa.alphabet:
            nfa.alphabet.append(self.sym)
        return nfa
        pass
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        nfa=NFA()
        nfa.states=[State(0)]
        nfa.is_accepting[0]=True
        return nfa
        pass
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()
