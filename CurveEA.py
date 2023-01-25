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
                choice=random.choice(['add','remove','change','shuffle'])

                if choice=='add':

                    mutation_n=random.randint(1,int(len(mutated_C[i][0])**1/2))
                    mutation_addition=[]
                    for _ in range(mutation_n):
                        x=round(random.uniform(-L/2,L/2),6)
                        y=round(random.uniform(-H/2,H/2),6)
                        z=round(random.uniform(-B/2,B/2),6)
                        if [x,y,z] not in mutation_addition:
                            mutation_addition.append([x,y,z])

                    mutated_C[i][0]=mutated_C[i][0].extend(mutation_addition)
                    mutated_C[i][1]=generate_edges(mutated_C[i][0])

                elif choice=='remove':
                    
                    if len(mutated_C[i][0])<6:
                        n = random.randint(1, int(len(mutated_C[i][0])-2))
                    else:
                        n = random.randint(1, int(len(mutated_C[i][0])**1/2))
                        
                    for _ in range(n):
                        mutated_C[i][0].pop(random.randint(0, len(mutated_C[i][0])-1))
                   
                    mutated_C[i][1]=generate_edges(mutated_C[i][0])

                elif choice=='change':

                    mutation_n=random.randint(1,int(len(mutated_C[i][0])**1/2))
                    for _ in range(mutation_n):
                        x=round(random.uniform(-L/2,L/2),6)
                        y=round(random.uniform(-H/2,H/2),6)
                        z=round(random.uniform(-B/2,B/2),6)
                        new_vertex=[x,y,z]
                        if new_vertex not in mutated_C[i][0]:
                            mutated_C[i][0][random.randint(0, len(mutated_C[i][0])-1)]=new_vertex
                    
                    mutated_C[i][1]=generate_edges(mutated_C[i][0])

                elif choice=='shuffle':
                    
                    print(mutated_C[i][0])
                    random.shuffle(mutated_C[i][0])
                    print(mutated_C[i][0])
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

