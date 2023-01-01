import random

def generate_rgbaRo(seed):
    random.seed(seed)
    
    # Randomly generate R,G,B,A and Roughness Factor
    R=random.randint(0,255) #Red
    G=random.randint(0,255) #Green
    B=random.randint(0,255) #Blue
    A=random.randint(0,255)   #Alpha (Opacity)
    RoughnessFactor=random.randint(0,5)
    
    return R,G,B,A,RoughnessFactor

def generate_vertices(L,B,H,seed):
    random.seed(seed)
    
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

def generate_faces(numOfVertices,seed):
    random.seed(seed)
    
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
                FACES.add(tuple(face))
      
    
    return list(FACES)

def generate_chromosome(L,B,H,seed):
    '''
    L -> Length of the bounding frame of model to be generated
    B -> Breadth of the bounding frame of model to be generated
    H -> Height of the bounding frame of model to be generated
    seed -> Manauly set random seed for each chromosome in the population 
    '''
    
    r,g,b,a,RoughnessFactor=generate_rgbaRo(seed)
    
    VERTICES=generate_vertices(L,B,H,seed)
    
    FACES=generate_faces(len(VERTICES),seed)
    
    return [r,g,b,a,RoughnessFactor,[VERTICES,FACES]]

def get_stats(CH):
    print(f'(R,G,B,A) = ({CH[0]},{CH[1]},{CH[2]},{CH[3]})')
    print(f'Roughness Factor = {CH[4]}')
    print(f'Number of vertices = {len(CH[5][0])}')
    print(f'Number of faces = {len(CH[5][1])}')
    