# -*- coding: utf-8 -*-
import numpy as np
import random
import Queue



def solve(board, pents):
    
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy array``s. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """
    pentDict = dict()
    check=1
    for pent in pents:
        pentDict.update({check:pent})
        check=check+1

    #precomputation
    choices=createChoices(board,pents,pentDict)
    constraints=createConstraints(board,pents,choices)

    # f1=open('./testfile.txt', 'w+')
    # f1.write(str(constraints))
    # f1.close()


    # for i in constraints:
    #     print "keys: ",i
    #     print "values: ",constraints[i]

    # for i in choices:
    #     print "keys: ",i
    #     print "values: ",choices[i]


    solution=[]
    print algoX(choices,constraints,solution)

    
    raise NotImplementedError

def algoX (curr_choices, curr_constraints,  curr_results):
    if len (curr_constraints) == 0: # problem has been solved
        return curr_results
    #pick the constraint with the fewest remaining choices
    constraint_queue = Queue.PriorityQueue
    for constraint in curr_choices.keys():
        constraint_queue.put((-len(curr_choices[constraint]), constraint))
    next_constraint = constraint_queue.get()[1]
    # pick the list of choices associated with the constraint
    next_choices = curr_choices[next_constraint]
    if len(next_choices) == 0:
        return -1 #problem cannot be solved from this point, need to backtrack
    #prioritizeing the available choices based on number of constraints associated
    choice_queue = Queue.PriorityQueue
    for choice in next_choices:
        choice_queue.put((-len(curr_constraints[choice]), choice))
    while choice_queue.empty() == False:
        next_choice = choice_queue.get()[1] #the the next value from priority queue
        #the following code removes the associated choices and constraints, and passes 
        #temp_choices and temp_constraints to the next algoX call
        temp_choices = curr_choices.copy()
        temp_constraints = curr_constraints.copy()
        satisfied_constraint_set = curr_constraints[next_choice]
        temp_results = curr_results.copy()
        for satisfied_constraint in satisfied_constraint_set:
            for satisfied_choice in curr_choices[satisfied_constraint]:
                temp_constraints.pop(satisfied_choice)
                #appends current change information to the result
                temp_results.append((satisfied_choice, satisfied_constraint))
            temp_choices.pop(satisfied_constraint)
        next_result = algoX(temp_choices, temp_constraints, curr_results)
        if next_result == -1:
            continue
        else:
            return next_result
    return curr_results
     

# def algoX(choices,constraints,solution):
#     if (not constraints): #If the set of unsatisfied constraints is empty, the problem is solved. Yield the solution and return.
#         return (solution)
    

#     c=constraints.keys()[0] #Otherwise, choose an unsatisfied constraint c.
#     print c

#     satisfyC=set([])
#     print satisfyC
#     for i in constraints[c]:
#         if (i in choices):
#             satisfyC.add(i)

#     if (not satisfyC):
#         return

#     for i in satisfyC: #If there are no choices that satisfy this constraint, the problem cannot be solved from this position. Return.
#         #print "i: ",i
#         satisfyI=set([]) #Find constraints satisfied by i

#         for I in choices[i]:
#             if(I in constraints):
#                 satisfyI.add(I)

#         print(choices.key())
#         print(i)
#         #exit()
#         for j in satisfyI:
#             copyConstraints=constraints
#             copyChoices=choices            
#             for k in constraints[j]:
#                 del choices[k]
#             del constraints[j]
#             solution.append(i)
#             algoX(choices,constraints,solution)
#             constraint=copyConstraints
#             choices=copyChoices           

#     return 





#Find tiles covered by pent at location
def findCover(pentNum,pent,row,col,boardX,boardY):
    if (pent.shape[0]+row>boardX or pent.shape[1]+col>boardY): #check if out of bounds
        return -1
    ret=set([])
    #ret.add(str(pent))
    ret.add(pentNum)
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j]>0:
                ret.add((row+i,col+j))
    return ret  

# def orientPent(pent,ori):
#         switcher={
#             0: pent,
#             1: np.rot90(pent),
#             2: np.rot90(np.rot90(pent)),
#             3: np.rot90(np.rot90(np.rot90(pent))),
#             4: np.flip(pent),
#             5: np.flip(np.rot90(pent)),
#             6: np.flip(np.rot90(np.rot90(pent))),
#             7: np.flip(np.rot90(np.rot90(np.rot90(pent))))

#         }
#         return switcher.get(ori,"error")

def orientPent(pent,ori):
        switcher={
            0: pent,
            1: np.rot90(pent,1),
            2: np.rot90(pent,2),
            3: np.rot90(pent,3),
            4: np.flip(pent),
            5: np.flip(np.rot90(pent,1)),
            6: np.flip(np.rot90(pent,2)),
            7: np.flip(np.rot90(pent,3))

        }
        return switcher.get(ori,"error")

def createChoices(board,pents,pentDict):
    choices=dict()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            for pentNum in range (1,len(pents)):                
                for ori in range(8):
                    const_=findCover(pentNum,orientPent(pentDict[pentNum],ori),i,j,board.shape[0],board.shape[1])                    
                    if (const_ !=-1):
                        #choices.update({str([pent,ori,i,j]):const_})
                        choices.update({(pentNum,ori,i,j):const_})
    return choices
    

def createConstraints(board,pents,choices):
    constraints=dict()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            tmpCoord=set([])
            for pentNum in range(1,len(pents)):
                for ori in range (8):                    
                    if ((pentNum,ori,i,j) in choices) and ((i,j) in choices[(pentNum,ori,i,j)]):                        
                        tmpCoord.add((pentNum,ori,i,j))                                                        
            constraints.update({(i,j):tmpCoord})

    for pentNum in range(1,len(pents)):
        tmpPent=set([])
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                for ori in range (8): 
                    if ((pentNum,ori,i,j) in choices and  pentNum in choices[(pentNum,ori,i,j)]):
                        tmpPent.add((pentNum,ori,i,j))
        constraints.update({pentNum:tmpPent})


    return constraints