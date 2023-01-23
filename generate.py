import bpy
import random
import sys
from ast import literal_eval

my_input = sys.argv

FILE_NUM=my_input[4]

VERTS_FILE=my_input[5]

MATERIALS=literal_eval(my_input[6])

BD=my_input[7]
ME=my_input[8]
RO=my_input[9]
SS=my_input[10]

OUTPUT_PATH=my_input[11]

with open(OUTPUT_PATH+"\\"+VERTS_FILE, 'r') as f:
    VERTS = f.readlines()

VERTS=literal_eval(VERTS[0])


# Generate a random set of vertices
vertices = VERTS

# Create a new curve object and set the vertices
curve_data = bpy.data.curves.new('MyCurve', type='CURVE')
curve_data.dimensions = '3D'
curve_data.resolution_u = 2

polyline = curve_data.splines.new('BEZIER')
polyline.bezier_points.add(len(vertices)-1)
for i, vertex in enumerate(vertices):
    x, y, z = vertex
    polyline.bezier_points[i].co = (x, y, z)

polyline.use_cyclic_u = True

# Create an object for the curve and link it to the scene
curve_obj = bpy.data.objects.new('MyCurve', curve_data)
bpy.context.collection.objects.link(curve_obj)

# Extrude the curve to create a skin-like surface
curve_obj.data.splines[0].use_smooth = True
curve_obj.data.bevel_depth = BD

bpy.context.view_layer.objects.active = bpy.data.objects[0]

obj = bpy.data.objects["MyCurve"]

# Add the modifier to the object
modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')

#Set the value of the modifier (e.g. the number of subdivisions)
modifier.levels = SS

#material
mat = bpy.data.materials.new("MyMaterial")
mat.diffuse_color = MATERIALS
mat.metallic=ME
mat.roughness=RO

obj.data.materials.append(mat)
