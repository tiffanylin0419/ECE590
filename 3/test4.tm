#This is a three tape turing machine
Tapes:3
#we specify what is blank.  In this case _
Blank:_

# copy input to tape 2 with a leading _
# and pad tape 3 with a leading _
0:,,=1,,R_,R_
1:A,,=1,R,RA,;B,,=1,R,RB,;C,,=1,R,RC,;_,,=2,,L,

2:,A,=2,,L,;,B,=2,,L,;,C,=2,,L,;,_,=3,,R,

# count As reversely
3:,A,=3,,R,RX;,B,=3,,R,;,C,=3,,R,;,_,=4,,L,L

4:,B,X=4,,L,L_;,C,X=5,,L,L_;,A,=4,,L,;,_,_=6,,,

5:,,X=4,,,L_


6:Accept