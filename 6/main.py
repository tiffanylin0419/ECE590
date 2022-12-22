import copy
from regex import *
from state import * 
from nfa import *
from dfa import *

def findPath(nfa,states,ch):
    path=set()
    for i in states:
        if ch in nfa.states[i].transition:
            for j in nfa.states[i].transition[ch]:
                path.add(j.id)
    return path

def expandPath(d,path):
    ans=[]
    for i in path:
        ans.append(i)
        for j in d[i]:
            ans.append(j)
    return set(ans)


def existPos(path,nfa_info) :
    i=0
    for i in range(len(nfa_info)):
        if path==nfa_info[i]:
            break
        i+=1
    return i

def containAccept(acceptings,states):
    for i in states:
        if acceptings[i]==True:
            return True
    return False
    
# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    #dictionary
    d={}
    for i in range(len(nfa.states)):
        ss=set([nfa.states[i]])
        while(ss!=nfa.epsilonClose2(ss)):
            ss=nfa.epsilonClose2(ss)
        allep=[]
        allep.append(i)
        for j in ss:
            allep.append(j.id)
        d[i]=set(allep)
    
    #dfa
    dfa=DFA()
    dfa.alphabet=nfa.alphabet


    state_len=0
    dfa.states.append(State(state_len))
    nfa_info=[d[0]]
    dfa.is_accepting[state_len]=containAccept(nfa.is_accepting,d[0])
    state_len+=1
    
    curr=0

    while(True):
        for ch in dfa.alphabet:
            s=findPath(nfa,nfa_info[curr],ch)
            if s==set():
                continue
            s=expandPath(d,s)
            n=existPos(s,nfa_info)
            if n<state_len:
                dfa.addTransition(dfa.states[curr], dfa.states[n], ch)
            else:
                dfa.states.append(State(state_len))
                nfa_info.append(s)
                dfa.is_accepting[state_len]=containAccept(nfa.is_accepting,s)
                state_len+=1
                dfa.addTransition(dfa.states[curr], dfa.states[n], ch)
        curr+=1
        if curr>=state_len:
            break


    return dfa
    pass
# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa=NFA()
    nfa.states = copy.deepcopy(dfa.states)
    nfa.is_accepting= copy.deepcopy(dfa.is_accepting)
    nfa.alphabet =copy.deepcopy(dfa.alphabet)
    return nfa
    pass

def unionNFA(nfa1,nfa2):
    len1=len(nfa1.states)
    nfa1.addStatesFrom(nfa2)
    nfa1.addTransition(nfa1.states[0],nfa1.states[len1])
    for i in nfa2.alphabet:
        if i not in nfa1.alphabet:
            nfa1.alphabet.append(i)
    return nfa1
# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    dfa1=nfaToDFA(nfa1)
    dfa2=nfaToDFA(nfa2)
    dfa1.complement()#complement
    dfa2.complement()
    nfa1_c=dfaToNFA(dfa1)
    nfa2_c=dfaToNFA(dfa2)
    n1b2=unionNFA(nfa1_c,nfa2)
    n12b=unionNFA(nfa1,nfa2_c)
    dfa1b2=nfaToDFA(n1b2)
    dfa12b=nfaToDFA(n12b)

    dfa1b2.complement()#complement
    dfa12b.complement()

    
    for i in dfa1b2.is_accepting:
        if dfa1b2.is_accepting[i]==True:
            return False
    
    for i in dfa12b.is_accepting:
        if dfa12b.is_accepting[i]==True:
            return False
    return True
    pass


if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()


        #print(nfa,end="")
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(strRe, s, expected):
        #I add this three lines and changed testDFA(nfa,s,expected)
        re = parse_re(strRe)
        nfa = re.transformToNFA()

        
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        #test complement
        #dfa.complement()
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def testshortest(strRe, s):
        re = parse_re(strRe)
        nfa = re.transformToNFA()
        dfa=nfaToDFA(nfa)
        
        ss=dfa.shortestString()
        if s==ss:
            print("Equivalence(", strRe, ") = ", s, " as expected.")
        else:
            print("Equivalence(", strRe, ") = ", s, " but expected " , ss)
            pass
        pass
    
    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    #test your NFA:
    '''testNFA('&', '', True)
    testNFA('(&)', '', True)
    testNFA('&', 'a', False)
    testNFA('a', '', False)
    testNFA('a', 'a', True)
    testNFA('a', 'ab', False)
    testNFA('(a)', 'a', True)
    testNFA('((a))', 'a', True)
    testNFA('ab', 'ab', True)
    testNFA('abc', 'abc', True)
    testNFA('abcd', 'abcd', True)
    testNFA('a(bc)d', 'abcd', True)
    testNFA('a*', '', True)
    testNFA('a*', 'a', True)
    testNFA('a*', 'aaa', True)
    testNFA('a*b*', 'a', True)
    testNFA('a*b*', 'ab', True)
    testNFA('a*b*', 'b', True)
    testNFA('a*b*', 'aba', False)
    testNFA('a|b', '', False)
    testNFA('a|b', 'a', True)
    testNFA('a|b', 'b', True)
    testNFA('a|b', 'ab', False)
    testNFA('ab|cd', '', False)
    testNFA('ab|cd', 'ab', True)
    testNFA('ab|cd', 'cd', True)
    testNFA('ab|cd*', '', False)
    testNFA('ab|cd*', 'c', True)
    testNFA('ab|cd*', 'cd', True)
    testNFA('ab|cd*', 'cddddddd', True)
    testNFA('ab|cd*', 'ab', True)
    testNFA('((ab)|(cd))*', '', True)
    testNFA('((ab)|(cd))*', 'ab', True)
    testNFA('((ab)|(cd))*', 'cd', True)
    testNFA('((ab)|(cd))*', 'abab', True)
    testNFA('((ab)|(cd))*', 'abcd', True)
    testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    testNFA('((a|b)*|b)*', 'ababb', True)'''

    #test your DFA:
    '''testDFA('&', '', True)
    testDFA('(&)', '', True)
    testDFA('&', 'a', False)
    testDFA('a', '', False)
    testDFA('a', 'a', True)
    testDFA('a', 'ab', False)
    testDFA('(a)', 'a', True)
    testDFA('((a))', 'a', True)
    testDFA('ab', 'ab', True)
    testDFA('abc', 'abc', True)
    testDFA('abcd', 'abcd', True)
    testDFA('a(bc)d', 'abcd', True)
    testDFA('a*', '', True)
    testDFA('a*', 'a', True)
    testDFA('a*', 'aaa', True)
    testDFA('a*b*', 'a', True)
    testDFA('a*b*', 'ab', True)
    testDFA('a*b*', 'b', True)
    testDFA('a*b*', 'aba', False)
    testDFA('a|b', '', False)
    testDFA('a|b', 'a', True)
    testDFA('a|b', 'b', True)
    testDFA('a|b', 'ab', False)
    testDFA('ab|cd', '', False)
    testDFA('ab|cd', 'ab', True)
    testDFA('ab|cd', 'cd', True)
    testDFA('ab|cd*', '', False)
    testDFA('ab|cd*', 'c', True)
    testDFA('ab|cd*', 'cd', True)
    testDFA('ab|cd*', 'cddddddd', True)
    testDFA('ab|cd*', 'ab', True)
    testDFA('((ab)|(cd))*', '', True)
    testDFA('((ab)|(cd))*', 'ab', True)
    testDFA('((ab)|(cd))*', 'cd', True)
    testDFA('((ab)|(cd))*', 'abab', True)
    testDFA('((ab)|(cd))*', 'abcd', True)
    testDFA('((ab)|(cd))*', 'cdcdabcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    testDFA('((a|b)*|b)*', 'ababb', True)'''

    #test Equivalence:
    '''testEquivalence('((a|b)*|b)*','(b)((a|b)*|b)*',False)
    testEquivalence('a*','aa*',False)
    testEquivalence('a|b', 'a|((a|b)|b)', True)
    testEquivalence('(a|b)*', '(a|((a|b)|b))*', True)
    testEquivalence('&', '&&', True)
    testEquivalence('&', '&&a', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn',False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '((ab|cd)*|(de*fg|h(ij)*klm*m*n|q))*',True)'''

    #test shortest string:
    testshortest('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', "")
    testshortest('(&)', "")
    testshortest('aa*', "a")
    testshortest('a*b*', "")
    testshortest('ab|cd', "ab")
    testshortest('((ab)|(cd))*', "")
    testshortest('de*fg|h(ij)*klm*n|q', "q")
    testshortest('de*fg|h(ij)*klm*n', "dfg")
    testshortest('h(ij)*klm*n', "hkln")

    
    pass
    
