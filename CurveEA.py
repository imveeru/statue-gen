import random
import copy
from CurveCGen import *
import numpy as np

def mutate(C,L,B,H):  # sourcery skip: merge-comparisons
    '''
    C -> Chromosome
    L,B,H -> Length, Breadth and Height of the bounding frame
    '''
    
#     new_L=random.randint(1,L)
#     new_B=random.randint(1,B)
#     new_H=random.randint(1,H)
    
    mutated_C=copy.copy(C)
    for i in range(len(mutated_C)):
        # generating a random value and checking for threshold value
        if random.random()>0.5:
            
            # for COLOURS
            if i in [0,1,2,3]:
                mutated_C[i]=round(random.uniform(0,L),6)
            
            #for BD
            elif i==4:
                mutated_C[i]=round(random.uniform(0.75,1.75),6)
            
            #for ME
            elif i==5:
                mutated_C[i]=round(random.uniform(0,1.0),6)
                
            #for RO
            elif i==6:
                mutated_C[i]=round(random.uniform(0,0.5),6)
            
            #for SS
            elif i==7:
                mutated_C[i]=random.randint(0,6)
            
            #for VERTS and EDGES
            elif i==8:
                mutated_C[i][0]=generate_vertices(L,B,H)
                mutated_C[i][1]=generate_edges(mutated_C[i][0])
    
    return mutated_C

def crossover(C1,C2):
    
    c1=copy.copy(C1)
    c2=copy.copy(C2)
    
    # Choose a random crossover point
    crossover_point = random.randint(0, len(c1))
    
    for i in range(crossover_point,len(c1)):
        c1[i], c2[i] = c2[i], c1[i]
    
    return c1,c2

