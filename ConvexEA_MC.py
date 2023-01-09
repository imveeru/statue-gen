import random
import copy
from ConvexCGen import *
import numpy as np
from scipy.spatial import Delaunay

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

def calculate_smoothness(vertices, faces):
    smoothness = 0
    
    for face in faces:
        
        v1, v2, v3 = vertices[face]
        
        normal = np.cross(v2 - v1, v3 - v1)
        
        angle1 = np.arccos(np.dot(normal, v2 - v1) / (np.linalg.norm(normal) * np.linalg.norm(v2 - v1)))
        angle2 = np.arccos(np.dot(normal, v3 - v2) / (np.linalg.norm(normal) * np.linalg.norm(v3 - v2)))
        angle3 = np.arccos(np.dot(normal, v1 - v3) / (np.linalg.norm(normal) * np.linalg.norm(v1 - v3)))
        
        smoothness += angle1 + angle2 + angle3
    
    smoothness /= len(faces)
    
    return smoothness

def calculate_symmetry(vertices):
    # Calculate the center of the mesh
    center = np.mean(vertices, axis=0)

    # Calculate the distance of each vertex from the center
    distances = np.linalg.norm(vertices - center, axis=1)

    # Calculate the standard deviation of the distances
    std_dev = np.std(distances)

    return 1 - std_dev

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

def volume_tetrahedron(tetrahedron):
    matrix = np.array([
        tetrahedron[0] - tetrahedron[3],
        tetrahedron[1] - tetrahedron[3],
        tetrahedron[2] - tetrahedron[3]
    ])
    return abs(np.linalg.det(matrix))/6

def volume_of_shape(vertices):
    # sourcery skip: inline-immediately-returned-variable
    tri = Delaunay(vertices)
    tetrahedra = corners[tri.simplices]
    
    volume = sum(np.array([volume_tetrahedron(t) for t in tetrahedra]))
    
    return volume

def surface_area(vertices,faces):
    surfaceArea=0
    
    for f in faces:
        p1=vertices[f[0]]
        p2=vertices[f[1]]
        p3=vertices[f[2]]
        
        l1=(p2[0]-p1[0])**2+(p2[1]-p1[1])**2+(p2[2]-p1[2])**2
        l2=(p3[0]-p2[0])**2+(p3[1]-p2[1])**2+(p3[2]-p2[2])**2
        l3=(p1[0]-p3[0])**2+(p1[1]-p3[1])**2+(p1[2]-p3[2])**2
        
        
        area=(4*l1*l2-(l3-l2-l1)**2)/16
        
        surfaceArea+=area
    
    return surfaceArea

def fitness(vertices, faces,shape):
    volume=round(shape[0]*shape[2]*shape[2],6)
    shapeVolume=volume_of_shape(vertices)
    volumeOfEmptySpace=abs(volume-shapeVolume)
    
    goldenRatio=golden_ratio(vertices,faces)
    
    smoothness=calculate_smoothness(vertices,faces)
    
    symmetry=calculate_symmetry(vertices)
    
    numOfFaces=len(faces)
    
    return round((volumeOfEmptySpace+goldenRatio+smoothness+symmetry+numOfFaces)/5,6)
    
    