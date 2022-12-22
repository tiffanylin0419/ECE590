import copy

# State is a class with two fields:
# -id = an integer which is used as the unique identifier of the state 
# -transition = a dictionary mapping from (char/symbol + epsilon ) to a set of states
class State:   
    def __init__(self,id):
        self.id = id
        self.transition = dict()
        pass
    def copy(self, s):
        self.id = s.id
        self.transition = copy.deepcopy(s.transition)
    def __str__(self):
        print(self.id,":")
        for i in self.transition:
            print("  ",i,":",end="")
            for j in self.transition[i]:
                print(j.id,", ",end="")
            print("")
        return ""
    pass
