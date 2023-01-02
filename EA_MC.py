import random
import copy
import os
import zlib
import sys
from CGen import *

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
            
            # for colours R,G,B, and Alpha
            if i==0 or i==1 or i==2 or i==3:
                mutated_C[i]=random.randint(0,255)
            
            #for roughness factor
            elif i==4:
                mutated_C[i]=random.randint(0,5)
            
            #for vertices and faces
            elif i==5:
                verts=generate_vertices(L,B,H)
                faces=generate_faces(len(verts))
                mutated_C[i]=[verts,faces]
    
    return mutated_C

def mutate_edge(C,L,B,H):  # sourcery skip: merge-comparisons
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
            
            # for colours R,G,B, and Alpha
            if i==0 or i==1 or i==2 or i==3:
                mutated_C[i]=random.randint(0,255)
            
            #for roughness factor
            elif i==4:
                mutated_C[i]=random.randint(0,5)
            
            #for vertices and faces
            elif i==5:
                verts=generate_vertices(L,B,H)
                edges=generate_edges(len(verts))
                mutated_C[i]=[verts,edges]
    
    return mutated_C


def crossover(C1,C2):
    
    c1=copy.copy(C1)
    c2=copy.copy(C2)
    
    # Choose a random crossover point
    crossover_point = random.randint(0, len(c1))
    
    for i in range(crossover_point,len(c1)):
        c1[i], c2[i] = c2[i], c1[i]
    
    return c1,c2

def fitness(PATH):
    
    fitness=[]
    
    for file in os.listdir(PATH):
        
        if file.endswith('.blend'):
    
            with open(PATH+"\\"+file, mode="rb") as fin, open(PATH+"\\"+file[:-3]+"_compressed", mode="wb") as fout:
                data = fin.read()
                compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                orig=sys.getsizeof(data)
                comp=sys.getsizeof(compressed_data)
                fitness.append(orig/comp)
        
    return fitness

def face_count(FACES,RO):
    return len(FACES)*(4**RO)

def new_fitness(FACES,RO,VERTICES,SHAPE):
    return len(FACES)*(4**RO)+len(VERTICES)+SHAPE[1]+(SHAPE[0]*SHAPE[1]*SHAPE[2])

def fractal_dimension(FACES):
    
    def countFrequency(my_list):
        freq = {}
        for item in my_list:
            if (item in freq):
                freq[item] += 1
            else:
                freq[item] = 1

        return freq

    len_faces=[len(f) for f in FACES]
    unique_count=countFrequency(len_faces)
    #print(unique_count)
    res=0
    for key in unique_count:
        res+=(1/unique_count[key])
    
    return round(res,6)
