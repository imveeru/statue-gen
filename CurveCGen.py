import random
import scipy.spatial

def generate_rgbaRo():
    
    r=round(random.uniform(0,1),6)
    g=round(random.uniform(0,1),6)
    b=round(random.uniform(0,1),6)
    a=round(random.uniform(0.25,1),6)
    
    bd=round(random.uniform(0.75,1.75),6)
    me=round(random.uniform(0,1.0),6)
    ro=round(random.uniform(0,0.5),6)
    ss=random.randint(0,6)
    
    return r,g,b,a,bd,me,ro,ss

def generate_vertices(L,B,H):
    #random.seed(seed)
    
    volume=L*B*H
    
    #generate random number of vertices (min-3, max-volume of bounding frame)
    numOfVertices=random.randint(4,int(volume**(1/2)))
    
    #generate vertices array
    VERTICES=[]
    i=0
    while i<numOfVertices:
        x=random.uniform(0,L)
        y=random.uniform(0,H)
        z=random.uniform(0,B)
        if [x,y,z] not in VERTICES:
            VERTICES.append([x,y,z])
            i+=1
    
    return VERTICES

def generate_convex_faces(vertices):
    tri = scipy.spatial.ConvexHull(vertices)

    faces = [(tri.simplices[i, j], tri.simplices[i, (j+1)%3], tri.simplices[i, (j+2)%3]) for i in range(tri.simplices.shape[0]) for j in range(3)]

    unique_faces = []

    for f in faces:
        sorted_face = tuple(sorted(f))

        if sorted_face not in unique_faces:
            unique_faces.append(sorted_face)

    return unique_faces or generate_convex_faces(vertices)

def generate_chromosome(L,B,H):
    '''
    L -> Length of the bounding frame of model to be generated
    B -> Breadth of the bounding frame of model to be generated
    H -> Height of the bounding frame of model to be generated
    seed -> Manauly set random seed for each chromosome in the population 
    '''
    
    new_L=round(random.uniform(1,L),6)
    new_B=round(random.uniform(1,B),6)
    new_H=round(random.uniform(1,H),6)
    
    VERTICES=generate_vertices(new_L,new_B,new_H)
    
    FACES=generate_convex_faces(VERTICES)
    
    materials,RoughnessFactor=generate_rgbaRo(len(FACES))
    
    return [RoughnessFactor,[VERTICES,FACES,materials],[new_L,new_B,new_H]]
    

def get_stats(CH):
    print(f'Roughness Factor = {CH[0]}')
    print(f'Number of vertices = {len(CH[1][0])}')
    print(f'Number of faces = {len(CH[1][1])}')
    print(f'Number of materials = {len(CH[1][2])}')
    print(f'New Bounding Box - (L,B,H) = ({CH[2][0]},{CH[2][1]},{CH[2][2]})')
    