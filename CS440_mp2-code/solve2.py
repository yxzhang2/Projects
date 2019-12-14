# -*- coding: utf-8 -*-
import numpy as np
import random

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
    #precomputation
    choices=createChoices(board,pents)
    constraints=createConstraints(board,pents,choices)

    f1=open('./testfile.txt', 'w+')
    f1.write(str(constraints))
    f1.close()


    # for i in constraints:
    #     print "keys: ",i
    #     print "values: ",constraints[i]

    solution=[]
    print algoX(choices,constraints,solution)

    
    raise NotImplementedError

def algoX(choices,constraints,solution):
    localSol=solution
    if (not constraints): #If the set of unsatisfied constraints is empty, the problem is solved. Yield the solution and return.
        return (solution)
    

    c=constraints.keys()[1] #Otherwise, choose an unsatisfied constraint c.
    #print "c:",c

    satisfyC=set([])
    for i in constraints[c]:
        print i
        if (i in choices):
            satisfyC.add(i)
    #print satisfyC

    if (not satisfyC):
        return

    for i in satisfyC: #If there are no choices that satisfy this constraint, the problem cannot be solved from this position. Return.
        #print "i: ",i
        satisfyI=set([]) #Find constraints satisfied by i
        for I in choices[i.replace("\\n", "\n")]:
            #print I
            if(I in constraints):
                satisfyI.add(I)

        for j in satisfyI:
            copyConstraints=constraints
            copyChoices=choices            
            for k in constraints[j]:
                del choices[k]
            del constraints[j]
            localSol.append(i)
            algoX(choices,constraints,localSol)
            constraint=copyConstraints
            choices=copyChoices           

    return 

     





#Find tiles covered by pent at location
def findCover(pent,row,col,boardX,boardY):
    if (pent.shape[0]+row>boardX or pent.shape[1]+col>boardY): #check if out of bounds
        return -1
    ret=set([])
    ret.add(str(pent))
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j]>0:
                ret.add((row+i,col+j))
    return ret  

def orientPent(pent,ori):
        switcher={
            0: pent,
            1: np.rot90(pent),
            2: np.rot90(np.rot90(pent)),
            3: np.rot90(np.rot90(np.rot90(pent))),
            4: np.flip(pent),
            5: np.flip(np.rot90(pent)),
            6: np.flip(np.rot90(np.rot90(pent))),
            7: np.flip(np.rot90(np.rot90(np.rot90(pent))))

        }
        return switcher.get(ori,"error")

def createChoices(board,pents):
    choices=dict()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            for pent in pents:
                for ori in range(8):
                    const_=findCover(orientPent(pent,ori),i,j,board.shape[0],board.shape[1])
                    
                    if (const_ !=-1):
                        choices.update({str([str(pent),ori,i,j]):const_})
    return choices
    

def createConstraints(board,pents,choices):
    constraints=dict()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            tmpCoord=set([])
            for pent in pents:
                tmpPent=set([])
                for ori in range (8):
                    if ((str([str(pent),ori,i,j]) in choices) and ((i,j) in choices[str([str(pent),ori,i,j])])):
                        tmpCoord.add (str([str(pent),ori,i,j]))
                    if str([str(pent),ori,i,j]) in choices:
                        tmpPent.add(str([str(pent),ori,i,j]))
                constraints.update({str(pent):tmpPent})
            constraints.update({(i,j):tmpCoord})
    return constraints