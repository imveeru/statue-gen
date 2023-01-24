import random

def generate_rgbaRo():
    
    r=round(random.uniform(0,1),6)
    g=round(random.uniform(0,1),6)
    b=round(random.uniform(0,1),6)
    a=round(random.uniform(0.25,1),6)
    
    bd=round(random.uniform(0.75,2.75),2)
    me=round(random.uniform(0,1.0),6)
    ro=round(random.uniform(0,0.5),6)
    ss=random.randint(0,6)
    
    return r,g,b,a,bd,me,ro,ss

def generate_vertices(L,B,H):
    #random.seed(seed)
    
    volume=L*B*H
    
    #generate random number of vertices (min-2, max-volume of bounding frame)
    numOfVertices=random.randint(2,int(volume**(1/2)))
    
    #generate vertices array
    VERTICES=[]
    i=0
    while i<numOfVertices:
        x=round(random.uniform(0,L),6)
        y=round(random.uniform(0,H),6)
        z=round(random.uniform(0,B),6)
        if [x,y,z] not in VERTICES:
            VERTICES.append([x,y,z])
            i+=1
    
    return VERTICES

def generate_edges(vertices):  # sourcery skip: convert-to-enumerate
    #edges
    edges=[]
    i=1
    for j in range(len(vertices)-1):
        edges.append([j,i])
        i+=1
    
    return edges

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
    
    EDGES=generate_edges(VERTICES)
    
    r,g,b,a,bd,me,ro,ss=generate_rgbaRo()
    
    return [r,g,b,a,bd,me,ro,ss,[VERTICES,EDGES],[new_L,new_B,new_H]]
    

def get_stats(CH):
    print(f'(R, G, B, A) = ({CH[0]}, {CH[1]}, {CH[2]}, {CH[3]})')
    print(f'Number of vertices = {len(CH[8][0])}')
    print(f'Number of edges = {len(CH[8][1])}')
    print(f'Bevel Depth = {CH[4]}')
    print(f'Metallic = {CH[5]}')
    print(f'Roughness = {CH[6]}')
    print(f'Subsurface Level = {CH[7]}')
    print(f'New Bounding Box - (L,B,H) = ({CH[9][0]},{CH[9][1]},{CH[9][2]})')
    