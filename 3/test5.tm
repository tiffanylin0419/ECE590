
# tape 0 stores input, tape 1 stores the number of A
# tape 2 stores the number of B and C
Tapes:3
Blank:_

0:A,,=0,R,R1,S;B,,=0,R,S,R1;C,,=0,R,S,R2;_,_,_=1,L,L,L

1:,1,1=1,S,L_,L_;,1,2=1,S,L_,S1;,_,_=2,S,S,S
2:Accept