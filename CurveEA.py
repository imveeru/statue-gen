import random
import copy
from CurveCGen import *
import numpy as np

def mutate(C,L,B,H):    # sourcery skip: merge-comparisons
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
                mutated_C[i]=round(random.uniform(0,1),6)

            elif i==4:
                mutated_C[i]=round(random.uniform(0.75,1.75),6)

            elif i==5:
                mutated_C[i]=round(random.uniform(0,1.0),6)

            elif i==6:
                mutated_C[i]=round(random.uniform(0,0.5),6)

            elif i==7:
                mutated_C[i]=random.randint(0,6)

            elif i==8:
               
                #print('Actual',mutated_C[i][0])
                # print(mutated_C[i][1])

                new_verts=copy.copy(mutated_C[i][0])
                
                for j in range(len(new_verts)):
                    choice=random.choice(['add','remove','change'])
                    
                    if choice=="add":
                        x=round(random.uniform(-L/2,L/2),6)
                        y=round(random.uniform(-H/2,H/2),6)
                        z=round(random.uniform(-B/2,B/2),6)
                        new_verts.insert(j,[x,y,z])
                        j+=1
                    
                    elif choice=="remove":
                        if len(new_verts)-1 >= 4 and j<len(new_verts):
                            new_verts.pop(j)
                            j-=1
                    
                    elif choice=="change" and j<len(new_verts):
                        x=round(random.uniform(-L/2,L/2),6)
                        y=round(random.uniform(-H/2,H/2),6)
                        z=round(random.uniform(-B/2,B/2),6)
                        new_verts[j]=[x,y,z]
                        
                #print(mutated_C[i][0])
                mutated_C[i][0]=new_verts
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

