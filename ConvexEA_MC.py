import random
import copy
from ConvexCGen import *
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
            
            # for roughness factor
            if i==0:
                mutated_C[i]=random.randint(0,6)
            
            #for vertices and faces
            elif i==1:
                verts=generate_vertices(L,B,H)
                faces=generate_convex_faces(verts)
                materials=generate_rgbaRo(len(faces))
                mutated_C[i]=[verts,faces,materials]
    
    return mutated_C

def crossover(C1,C2):
    
    c1=copy.copy(C1)
    c2=copy.copy(C2)
    
    # Choose a random crossover point
    crossover_point = random.randint(0, len(c1))
    
    for i in range(crossover_point,len(c1)):
        c1[i], c2[i] = c2[i], c1[i]
    
    return c1,c2

def golden_ratio(vertices, faces):
      
  total_length = 0
  for face in faces:
    for i in range(len(face)):
      v1 = vertices[face[i]]
      v2 = vertices[face[(i+1) % len(face)]]
      total_length += np.linalg.norm(v1 - v2)
  avg_length = total_length / len(faces)
  
  
  min_length = float('inf')
  max_length = 0
  for face in faces:
    for i in range(len(face)):
      v1 = vertices[face[i]]
      v2 = vertices[face[(i+1) % len(face)]]
      edge_length = np.linalg.norm(v1 - v2)
      min_length = min(min_length, edge_length)
      max_length = max(max_length, edge_length)
  ratio = max_length / min_length
  
  
  golden_ratio = (1 + np.sqrt(5)) / 2
  deviation = abs(ratio - golden_ratio) / golden_ratio
  
  return 100 - deviation * 100