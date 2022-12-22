import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        print('states: ')
        for i in range(len(self.states)):
            print(self.states[i],end="")
        print('is_accepting: ')
        print(self.is_accepting)
        print('startS:',self.startS)
        return ""
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        s1.transition[sym]=[s2]
        pass 
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for i in self.is_accepting:
            self.is_accepting[i]=not self.is_accepting[i]
        pass
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        #dfa=self
        curr=0
        for i in string:
            if i not in self.states[curr].transition:
                return False
            else:
                curr=self.states[curr].transition[i][0].id
        return self.is_accepting[curr]
        pass
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        
        queue_num=[0]
        queue_str=[""]
        visited=[]
        while queue_num!=[]:
            curr_num=queue_num.pop(0)
            curr_str=queue_str.pop(0)
            if self.is_accepting[curr_num]:
                    return  curr_str
            if curr_num not in visited:
                visited.append(curr_num)
            for ch in self.states[curr_num].transition:
                queue_num.append(self.states[curr_num].transition[ch][0].id)
                queue_str.append(curr_str+ch)
            
        return ""
        pass
    pass
