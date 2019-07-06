
'''
Init the state variable
   <FSM>
   Clockwise rotation:AB
   11->01->00->10
   Counterclockwise rotation:AB
   11->10->00->01
'''
state = 00
print("Initial state is", state)

S1 = 00
S1 = 10
S2 = 11
S3 = 11

# cstate : current state
def getDirection(cstate) :
    if(state == 00 and cstate = 10) :
        return "clockwise"
    else :
        return "counterclockwise"
    if(state == 10 and cstate = 11) :
        return "clockwise"
    else :
        return "counterclockwise"
    if(state == 11 and cstate = 01) :
        return "clockwise"
    else :
        return "counterclockwise"
    if(state == 01 and cstate = 00) :
        return "clockwise"
    else :
        return "counterclockwise"