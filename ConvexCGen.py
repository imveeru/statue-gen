import random
import scipy.spatial

def generate_rgbaRo(numOfFaces):
    #random.seed(seed)
    materials=[]
    
    for _ in range(numOfFaces):
        # Randomly generate R,G,B,A and Roughness Factor
        R=random.uniform(0,1) #Red
        G=random.uniform(0,1) #Green
        B=random.uniform(0,1) #Blue
        A=random.uniform(0,1)   #Alpha (Opacity)
        
        materials.append(R,G,B,A)
    
    RoughnessFactor=random.randint(0,6)
    
    return R,G,B,A,RoughnessFactor

def generate_vertices(L,B,H):
    #random.seed(seed)
    
    volume=L*B*H
    
    #generate random number of vertices (min-3, max-volume of bounding frame)
    numOfVertices=random.randint(3,int(volume**(1/2)))
    
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

def generate_edges(numOfVertices):
    EDGES=[]

    for i in range(numOfVertices-1):
        
        j=random.choice(list(range(numOfVertices-1)))
        
        if (
            i != j
            and random.random() > 0.5
            and (i, j) not in EDGES
            and (j, i) not in EDGES
        ):
            EDGES.append((i, j))

    if EDGES:
        return EDGES
    else:
        return generate_edges(numOfVertices)

def generate_convex_faces(vertices):
    tri = scipy.spatial.ConvexHull(vertices)
    
    faces = [(tri.simplices[i, j], tri.simplices[i, (j+1)%3], tri.simplices[i, (j+2)%3]) for i in range(tri.simplices.shape[0]) for j in range(3)]
    
    unique_faces = []

    for f in faces:
        sorted_face = tuple(sorted(f))

        if sorted_face not in unique_faces:
            unique_faces.append(sorted_face)
     
    if len(unique_faces)>0:
        return unique_faces
    else:
        return generate_convex_faces(vertices)
 
def generate_faces(numOfVertices):
    #random.seed(seed)
    
    FACES=set()

    # A nested loop to iterate through all the vertices
    for i in range(numOfVertices):
        for j in range(i + 1, numOfVertices):
            '''
            Generating a random number between 0-1 and if it is greater than 0.5 (thresholding value) we proceed
            to make a connection, else skip to the next vertice.   
            '''
            if random.random() > 0.5:
                # Create a face by connecting the current vertex to all of the other vertices that it is connected to
                face = [i]

                #iterate through all the vertices other than the currently chosen one (i)
                for k in range(numOfVertices):
                    if (k != i) and (random.random() > 0.5):
                        face.append(k)

                # Add the face to the set of faces
                if len(face)>=3:
                    FACES.add(tuple(face))
      
    if len(FACES)>0:
        return list(FACES)
    else:
        return generate_faces(numOfVertices)

def generate_chromosome(L,B,H):
    '''
    L -> Length of the bounding frame of model to be generated
    B -> Breadth of the bounding frame of model to be generated
    H -> Height of the bounding frame of model to be generated
    seed -> Manauly set random seed for each chromosome in the population 
    '''
    
    r,g,b,a,RoughnessFactor=generate_rgbaRo()
    
    new_L=round(random.uniform(1,L),6)
    new_B=round(random.uniform(1,B),6)
    new_H=round(random.uniform(1,H),6)
    
    VERTICES=generate_vertices(new_L,new_B,new_H)
    
    FACES=generate_faces(len(VERTICES))
    
    return [r,g,b,a,RoughnessFactor,[VERTICES,FACES],[new_L,new_B,new_H]]

def generate_chromosome_edge(L,B,H):
    
    r,g,b,a,RoughnessFactor=generate_rgbaRo()
    
    new_L=round(random.uniform(1,L),6)
    new_B=round(random.uniform(1,B),6)
    new_H=round(random.uniform(1,H),6)
    
    VERTICES=generate_vertices(new_L,new_B,new_H)
    
    EDGES=generate_edges(len(VERTICES))
    
    return [r,g,b,a,RoughnessFactor,[VERTICES,EDGES],[new_L,new_B,new_H]]
    

def get_stats(CH):
    print(f'(R,G,B,A) = ({CH[0]},{CH[1]},{CH[2]},{CH[3]})')
    print(f'Roughness Factor = {CH[4]}')
    print(f'Number of vertices = {len(CH[5][0])}')
    print(f'Number of faces = {len(CH[5][1])}')
    print(f'New Bounding Box - (L,B,H) = ({CH[6][0]},{CH[6][1]},{CH[6][2]})')
    