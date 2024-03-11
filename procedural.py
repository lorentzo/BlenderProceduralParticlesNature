
import bpy
import mathutils

# Vertex groups are created per object.
# Each vertex group element can be read/write from object.
# Each vertex group element can be read from vertex.
# bpy.types.object.vertex_groups (https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.vertex_groups)
# bpy.types.VertexGroups (https://docs.blender.org/api/current/bpy.types.VertexGroups.html)
# bpy.types.VertexGroup https://docs.blender.org/api/current/bpy.types.VertexGroup.html
# bpy.types.Object.data -> bpy.types.mesh (if object contains mesh) https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.data
# bpy.types.mesh.vertices (https://docs.blender.org/api/current/bpy.types.Mesh.html#bpy.types.Mesh.vertices)
# bpy.types.MeshVertex.groups https://docs.blender.org/api/current/bpy.types.MeshVertex.html#bpy.types.MeshVertex.groups
# bpy.types.VertexGroupElement https://docs.blender.org/api/current/bpy.types.VertexGroupElement.html#bpy.types.VertexGroupElement

for obj in bpy.data.collections["LittlePlanet"].all_objects:
    nVertGroupsToCreate = len(obj.particle_systems) # equals to the number of particle systems!
    print("Checking if object has existing vertex groups...")
    # bpy_struct.items() returns the items of this objects custom properties (matches Python’s dictionary function of the same name).
    # https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.items
    if len(obj.vertex_groups.items()) <= 0:
        print("Object contains no vertex groups!")
    else:
        print("Object contains vertex groups! Removing existing vertex groups!", len(obj.vertex_groups.items()))
        existing_vertex_groups = []
        for vg_idx in range(len(obj.vertex_groups.items())):
            existing_vertex_groups.append(obj.vertex_groups[vg_idx])
        while existing_vertex_groups:
            obj.vertex_groups.remove(existing_vertex_groups.pop())
    
    print("Creating new vertex groups...")
    for i in range(nVertGroupsToCreate):
        group = obj.vertex_groups.new( name = str(i) )
        print("Created vertex group", str(i))

    print("Populating vertex groups...")
    for vert in obj.data.vertices:
        v_co = vert.co
        v_groups = vert.groups # read only
        v_idx = vert.index
        for vg in obj.vertex_groups:
            vg_idx = vg.index
            # https://docs.blender.org/api/current/mathutils.noise.html
            H = 1.2 + int(vg_idx)
            lacunarity = 2 + int(vg_idx)
            octaves = 2 + int(vg_idx)
            #vert_weight = 1.0-mathutils.noise.multi_fractal(v_co, H, lacunarity, octaves, noise_basis='PERLIN_ORIGINAL') * 0.9
            hardTransitions = True
            offset = 0.5
            v_co_perturbed = mathutils.Vector((v_co[0] + int(vg_idx) + offset, v_co[1] + int(vg_idx) + offset, v_co[2] + int(vg_idx) + offset))
            vert_weight = mathutils.noise.turbulence(v_co_perturbed, octaves, hardTransitions, noise_basis='BLENDER', amplitude_scale=3, frequency_scale=0.1)
            vg.add([v_idx], vert_weight, "REPLACE")
            print("For vertex", v_idx, "populating group", vg_idx, "with", vert_weight)

    print("Updating particle systems...")
    i = 0
    for ps in obj.particle_systems:
        ps.vertex_group_length = str(i)
        ps.vertex_group_density = str(i)
        i += 1

            
            

        
        
