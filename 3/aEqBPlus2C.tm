#This is a three tape turing machine
Tapes:3
#we specify what is blank.  In this case _
Blank:_
#We start by putting a _ before input (and we'll get one after
#explicitly by looking there)
#abc => _abc_
0:A,,=1,R_,,;B,,=2,R_,,;C,,=3,R_,,;_,,=4,,,
#previous thing we are moving is an A
1:A,,=1,RA,,;B,,=2,RA,,;C,,=3,RA,,;_,,=5,LA,,
#previous thing we are moving is a B
2:A,,=1,RB,,;B,,=2,RB,,;C,,=3,RB,,;_,,=5,LB,,
#previous thing we are moving is a C
3:A,,=1,RC,,;B,,=2,RC,,;C,,=3,RC,,;_,,=5,LC,,
4:Reject
# Looking for the starting dot
# when we find it, go to 6 and put _ on all three tapes
# and move right
5:A,,=5,LA,,;B,,=5,LB,,;C,,=5,LC,,;_,,=6,R_,R_,R_
#when we see an A or a B we mark it on tape 1 (A) or 2 (B)
# and stay in 6
# when we see a C, we mark it on tape 2, and go to 7 to make
# another mark
6:A,,=6,RA,R1,;B,,=6,RB,,R1;C,,=7,RC,,R1;_,,=8,L,L,L
#then just mark it and go back to 6
7:,,=6,,,R1
#Now we've counted them up, so we need to go backwards and see if they are equal
8:,1,1=8,,L,L;,1,_=4,,,;,_,1=4,,,;,_,_=9,,,
9:Accept