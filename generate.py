import bpy
import random

# Generate a random set of vertices
num_vertices = 15
vertices = [
    (random.uniform(-5, 5), random.uniform(-3, 3), random.uniform(-8, 8))
    for _ in range(num_vertices)
]

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
curve_obj.data.bevel_depth = 0.75

#bpy.data.objects['MyCurve'].select_set(True) 
#bpy.context.view_layer.objects.active = obj
bpy.context.view_layer.objects.active = bpy.data.objects[0]
#bpy.ops.object.convert(target='MESH')

#bpy.context.view_layer.objects.active = bpy.data.objects["MyCurve"]
#bpy.ops.object.convert()
obj = bpy.data.objects["MyCurve"]

# Add the modifier to the object
modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')

#Set the value of the modifier (e.g. the number of subdivisions)
modifier.levels = 6
COLOUR=(0.0196078431372549, 0.6862745098039216, 0.0784313725490196, 0.2)
mat = bpy.data.materials.new("MyMaterial")
mat.diffuse_color = COLOUR

obj.data.materials.append(mat)
