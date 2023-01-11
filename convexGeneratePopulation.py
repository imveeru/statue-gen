import sys
import bpy
from ast import literal_eval

my_input = sys.argv

FILE_NUM=my_input[4]

VERTS_FILE=my_input[5]
FACES_FILE=my_input[6]
MATERIALS_FILE=my_input[7]

RO=int(my_input[8])
OUTPUT_PATH=my_input[9]

with open(OUTPUT_PATH+"\\"+VERTS_FILE, 'r') as f:
    VERTS = f.readlines()

VERTS=literal_eval(VERTS[0])
    
with open(OUTPUT_PATH+"\\"+FACES_FILE, 'r') as f:
    FACES = f.readlines()

FACES=literal_eval(FACES[0])

with open(OUTPUT_PATH+"\\"+MATERIALS_FILE, 'r') as f:
    MATERIALS = f.readlines()

MATERIALS=literal_eval(MATERIALS[0])    
    
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj) 


# Create a new mesh and object
mesh = bpy.data.meshes.new("15000")
object = bpy.data.objects.new("15000", mesh)

# Set the location and scene of the object
object.location = (0,0,0)
bpy.context.collection.objects.link(object)


vertices=VERTS
faces=FACES

# Add the vertices and faces to the mesh
mesh.from_pydata(vertices, [], faces)

materials=MATERIALS

for i, face in enumerate(mesh.polygons):
    # Create a new material
    mat = bpy.data.materials.new(name=f"Face {i}")
    
    material=materials[i]

    # Assign a random color to the material
    mat.diffuse_color = (material[0],material[1],material[2],material[3])

    # Add the material to the object's material slots
    object.data.materials.append(mat)

# Update the material indices of the faces
x=0
for i, face in enumerate(mesh.polygons):
    face.material_index = i
    x+=1
    
RO=2

object.modifiers.new("subd", type='SUBSURF')
object.modifiers['subd'].levels = RO

bpy.ops.object.shade_smooth()

mypolys = mesh.polygons
for p in mypolys:
    p.use_smooth = True

mesh.update()

bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_PATH+"\\STATUE_"+FILE_NUM+'.blend')
