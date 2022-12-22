import sys
#Input format
#Tapes: num
#Blank: sym  [what we read on tape after end of input]
#Then a state line is either
#  num:Accept
#  num:Reject
#  num:info;info;...;info
# where info has sym?,...,sym?=statenum,act,..,act
#   The number of syms on the left corresponds to the number of tapes
#   The number of acts on the right corresponds to the number of tapes.
#     - sym is any input symbol.  Note that the following characters are special
#            ,;:
#       so we don't allow them to be used.   , ; and : are field delimieters
#       If the symbol is ommitted, it means "we dont care".  E.g. A,,B,C,,D
#       matches an A on tape 0, a B on tape 2, a C on tape 3, a D on tape 5,
#       and does not care what is on tapes 1 or 4.
#     - act is
#         [R|S|L]sym
#         Where R means "move right", S means "stay" and L means "move left"
#         sym is the symbol to write on the tape (before moving)
#         Note that a single character [R|S|L] means "keep the same symbol"
#         Nothing at all means "stay and keep the same symbol"

# Now let us start to represent our TM in code


# This is three-field struct for a transition.
# It is constructed from three pieces of information:
# (1) state: is an integer specfiying the state number to go to
# (2) syms: is a list of the symbols to write to the tapes.  Note that
#           this list is one entry per tape, and an entry may be None
#           which indicates that nothing should be written to that tape
# (3) movement: is a list of 'R' (move right), 'S' (stay here) and 'L' (move left)
#           This list also has one entry per tape.
class Transition:
    # This is the constructor.  It "builds" one of these object.
    # You don't call it directly, but instead do
    # t = Transition(state, syms, movements)
    def __init__(self, state, syms, movements):
        self.state = state
        self.movements = movements
        self.syms = syms
        pass

    # This function specifies how to convert this object to a string
    # You dont call it directly, but instead do str(t) (where t is
    # the thing you want to convert to a string)
    def __str__(self):
        ans = ' => {:2d} ['.format(self.state)
        sep = ''
        for i in range(0, len(self.movements)):
            ans = ans + sep + self.movements[i]
            if self.syms[i] is not None:
                ans = ans + self.syms[i]
            else:
                ans = ans + ' '
                pass
            sep = ', '
            pass
        return ans + ']'

    pass


# This is a three-field struct for a state.
# It is constructed from three pieces of information
# (1) A boolean indicating if this state is an Accept state
# (2) A boolean indicating if this state is a Reject state
# (3) A list which specifies what Transitions to take under what conditions
#     Each item in this list is a 2-tuple (match, transition).
#     Where "match" is a list of (tape symbol | None), which has one item per tape
#     Here, None means "we dont care what is on that tape" and anything else
#     means that we want to match that symbol.
#     For example ['A', None, 'B'] means that tape 0 needs an 'A',
#     we don't care what is on tape 2 needs a 'B'.
#     Matching is done in order (the first match that succeeds is taken)
#     and when a match is found, the corresponding Transition is executed.
#     If no match is found, the TM should reject (right away).
#     (as if every state has an implicit rule:
#      ([None, ...None],Transition(reject_state,[None,...None],['S',...'S']))


class State:
    def __init__(self, is_accept, is_reject, transitions):
        self.is_accept = is_accept
        self.is_reject = is_reject
        assert not is_accept or not is_reject, "A state cannot be both accepting and rejecting!"
        self.transitions = transitions
        pass

    def __str__(self):
        if self.is_reject:
            return "Reject"
        if self.is_accept:
            return "Accept"
        ans = ''
        sep = '{ '
        for (m, t) in self.transitions:
            ans = ans + sep + str(m) + str(t)
            sep = '\n  '
            pass
        ans = ans + '\n}'
        return ans

    pass


# This class  (think struct) represents a Turing Machine
# has three fields.
# states is a list of State objects (as above)
# blank_char is the character that we consider "blank"
#    Whenever this TM moves past the end of any of its current tapes.
#    that tape is extended with a blank_char
# num_tapes is the number of tapes that this TM has.


class TuringMachine:
    def __init__(self, states, blank_char, num_tapes):
        self.states = states
        self.blank_char = blank_char
        self.num_tapes = num_tapes
        pass

    def __str__(self):
        ans = 'A Turing Machine with ' + str(
            self.num_tapes) + " tapes and blank char " + self.blank_char
        for i in range(0, len(self.states)):
            ans = ans + "\nState " + str(i) + ": \n"
            ans = ans + str(self.states[i])
            pass
        return ans

    pass


# This takes the 2,R_,, part of an input line---i.e.
# the transition information after a match is found
# and returns a Transition object
def parseTransition(tinfo, num_tapes):
    x = tinfo.strip().split(',')
    assert len(
        x
    ) == num_tapes + 1, "Expected transition info to have 1 state + " + str(
        num_tapes) + " of info, but found " + tinfo
    snum = int(x[0])
    movements = []
    writes = []
    for i in x[1:]:
        assert len(i) <= 2, "Info too long for one tapes actions: " + i
        m = i[0] if len(i) > 0 else 'S'
        assert m == 'R' or m == 'S' or m == 'L', "Invalid movement letter: " + m
        w = i[1] if len(i) > 1 else None
        movements.append(m)
        writes.append(w)
        pass
    return Transition(snum, writes, movements)


# The input line will look like this (for a 3 tape TM)
# 0:A,,=1,R_,,;B,,=2,R_,,;C,,=3,R_,,;_=4,,,
# but we will only get the part after the : in this function
# We split that up by ; which describes the transitions, e.g.,
# A,,=1,R_,,
# B,,=2,R_,,
# C,,=3,R_,,
# _,,=4,,,
# each of those has two parts.  The "match" on the left (e.g. A,,)
# and the transition (on the right) (e.g., 1,R_,,)
# The match specifies the the input symbols on each tape, or
# blank for None (dont care).  The transition specifies the state
# number forllowed by pairs of (R|S|L) and the symbol to write.
# If the symbol is ommitted, "keep the same" is implicit.
# If the direction is ommitted, Stay is implicit.
# Note that sinfo could also be "Accept" or "Reject"
# This function returns a State object.
def parseState(sinfo, num_tapes):
    if sinfo == "Accept":
        return State(True, False, [])
    if sinfo == "Reject":
        return State(False, True, [])
    ans = []
    for piece in sinfo.split(';'):
        parts = piece.split('=')
        assert len(
            parts
        ) == 2, "Invalid transition info: " + piece + " from " + sinfo + " expected exactly one ="
        match = [None if x == '' else x for x in parts[0].split(",")]
        assert len(match) == num_tapes, "Invalid match " + parts[
            0] + " expected info for " + str(num_tapes) + " tapes"
        transition = parseTransition(parts[1], num_tapes)
        ans.append((match, transition))
        pass
    return State(False, False, ans)


def readTM(fname):
    num_tapes = None
    blank_char = None
    states = {}
    max_state = 0
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if (line == "" or line[0] == "#"):
                continue
            parts = line.split(":")
            assert len(
                parts
            ) == 2, "Error processing line " + line + " expected exactly one :"
            if parts[0] == "Tapes":
                assert num_tapes is None, "Error: number of tapes specified twice"
                num_tapes = int(parts[1])
                continue
            if parts[0] == "Blank":
                assert blank_char is None, "Error: blank char specified twice"
                blank_char = parts[1][0]
                continue
            snum = int(parts[0])
            max_state = max(snum, max_state)
            states[int(parts[0])] = parseState(parts[1], num_tapes)
            pass
        pass
    state_list = [
        states[i] if i in states else State(False, True, [])
        for i in range(0, max_state + 1)
    ]
    return TuringMachine(state_list, blank_char, num_tapes)


# This function prints your Turing Machine at each
# step in the execution.
# It takes
#   state: an integer specifying the current state
#   tapes: a list with each tape (each tape should be a list of characters)
#   tape_pos: a list of integers, specifying the current position on each tape
def printTmExec(state, tapes, tape_pos):
    print("The TM is in state " + str(state))
    for i in range(0, len(tapes)):
        print("Tape {:2d} has ".format(i), end='')
        for j in tapes[i]:
            print(j, end='')
            pass
        print()
        for j in range(0, tape_pos[i] + 12):
            print(' ', end='')
            pass
        print('^')
        pass
    pass


# Here are three helper functions I found useful to write.
# You do not have to write them, but you might find them useful:
# 1. def ensureTapesHaveBlanks(tapes, tape_pos, blank_char):
#      Given the tapes, and positions, ensure that we add any blanks
#      onto the end that we might need.  Remember that a TM has an infinite
#      tape, so when we "go off the right end" we just add another blank_char.

# 3. def findMatch(transitions, syms):
#      Given the transitions from the current state (e.g. current_state.transitions)
#      And a list with the symbols on each tape,
#      Look through the transitions and find the right match.
#      If found, I returned the corresponding transition,
#      If nothing was found, I returned None

def move_incr_from_letter(letter):
    # Convert a letter (like R, S, or L) into a number that
    # specifies how we change the position on the tape
    if letter =='L':
        return -1
    if letter =='S':
        return 0
    if letter =='R':
        return 1


# This function (which you will write)
# executes a turing machine (tm) on a given input (s).
# The third parameter (verbose) specifies whether or not
# you should print the current state number + contents of the
# tape at each step in the execution.
# This function should return True if TM accepts s,
# and False if TM rejects s.
# Note that this function should go into an infinite
# loop iff the execution of tm on s does not halt.
def executeTM(tm, s, verbose):
    
    # Replace this with your code!
    
    #verbose
    state=0
    tapes=[s]
    tape_num=tm.num_tapes
    for i in range(tape_num-1):
        tapes.append('')
    tape_pos=[0]*tape_num
    while True:
        # ensureTapesHaveBlanks
        for j in range(tape_num):
            if tape_pos[j]>=len(tapes[j]):
                tapes[j]+=tm.blank_char
        # print
        if verbose:
            printTmExec(state, tapes, tape_pos)
        #print("test:",tm.states[0].is_accept,tm.blank_char,tm.num_tapes)
        
        # accept or reject
        if tm.states[state].is_accept:
            return True
        if tm.states[state].is_reject:
            return False
        # find match and change state and tape info
        tran=tm.states[state].transitions
        #print(tran)
        passed=False
        for i in range(len(tran)):
            can_pass=True
            for j in range(tape_num):
                #print(tran[i][0][j])
                if tran[i][0][j]!=None and tapes[j][tape_pos[j]]!=tran[i][0][j]:
                    can_pass=False
            if can_pass:
                passed=True
                state=tran[i][1].state
                for j in range(tape_num):
                    if tran[i][1].syms[j]!=None:
                        lst=list(tapes[j])
                        lst[tape_pos[j]]=tran[i][1].syms[j]
                        tapes[j]=''.join(lst)                  
                    tape_pos[j]+=move_incr_from_letter(tran[i][1].movements[j])
                break
        if not passed:
            return False
            
    

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage python3 tm.py tmfile inputstr [verbose]")
        sys.exit(1)
        pass
    fname = sys.argv[1]
    t = readTM(fname)
    s = sys.argv[2]
    v = len(sys.argv) >= 4
    if (v):
        print(t)
        pass
    res = executeTM(t, s, v)
    print("Answer: " + str(res))
    pass

