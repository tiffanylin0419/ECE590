#This Turing Machine looks for "double palindromes" with only a,b,c.
#e.g. abccbaabccba
# Is the same forward as backwards, but also if we cut it in half,
# then one half (abccba) is also a palindrom
#This is a two tape turing machine
Tapes:2
#we specify what is blank.  In this case _
Blank:_

#When we start, if we see (blank) we are done (empty string),
#so we go to state 1 (Accept).
#Otherwise, we need to move Right on tape 2 (we explicitly write
#blank, but that write could be implicit) and go to state 2 to
#start doing the work.
0:_,=1,,;,=2,,R_

#Our accept state.  Note that we do reject strings,
#we are just exploiting our "default reject on match fail"
#in other states
1:Accept

#This state is where we look at the left most
#character currently left in the string, remember
#is in our state (a=3, b=5, c=7), cross it off (replace
#with blank) and start moving Right
#Note that if the leftmost character is _ we are
#done with the first step of processing, so we go
#to 18
2:_,=18,,L;a,=3,R_,;b,=5,R_,;c,=7,R_,

#This is the "we saw an a on the left" state
#so we move right until _, then go back one
3:a,=3,R,;b,=3,R,;c,=3,R,;_,=4,L,

#looking for an "a"---if we see it, go to
#9 (scan back left) and note the a on the other tape
#Any input other than "a" is reject (implicitly by not match)
4:a,=9,L_,Ra

#saw a "b"---look for _ then back
5:a,=5,R,;b,=5,R,;c,=5,R,;_,=6,L,

#did we find a "b"?
6:b,=9,L_,Rb

#saw a "c"---look for _ then back
7:a,=7,R,;b,=7,R,;c,=7,R,;_,=8,L,

#did we find a "c"?
8:c,=9,L_,Rc

#scan back to the left
9:_,=2,R_,;,=9,L,

#This state is where we start doing the palindrome
#algorithm on Tape 2.  If we see blank, we are done.
#Otherwise, we use state number to remember if we
#saw "a", "b" or "c".  We "cross off" whichever
#letter we see
10:,_=1,,;_,a=11,,R_;_,b=13,,R_;_,c=15,,R_

#This state is where we saw an "a" and
#are scanning right for the end
11:,a=11,,R;,b=11,,R;,c=11,,R;,_=12,,L

# This state is where we make sure we have an "a"
# and if so, cross it off
12:,a=17,,L_

#This state is where we saw an "b" and
#are scanning right for the end
13:,a=13,,R;,b=13,,R;,c=13,,R;,_=14,,L

# This state is where we make sure we have an "b"
# and if so, cross it off
14:,b=17,,L_

#This state is where we saw an "c" and
#are scanning right for the end
15:,a=15,,R;,b=15,,R;,c=15,,R;,_=16,,L

# This state is where we make sure we have an "c"
# and if so, cross it off
16:,c=17,,L_

# This state is where we can back to the left
# before we restart in 10 for the next pair of letters
17:,_=10,,R;,=17,,L

# At this point, we know the input was a palindrome
# and have written half of it onto Tape 2.
# we now basically redo the palindrome algorithm on Tape 2.
# But first we have to move the Tape position of Tape 2
# all the way left.
# (Note: we could have just done the palindrome algorithm
# backwards instead of seeking left if we wanted).
18:,_=10,,R;,=18,,L