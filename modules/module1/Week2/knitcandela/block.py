import os
import sys
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.datastructures import mesh_flip_cycles

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

mesh_flip_cycles(cablenet)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.200

# ==============================================================================
# Make block
# ==============================================================================

fkey = cablenet.get_any_face()

vertices = cablenet.face_vertices(fkey)

points = cablenet.get_vertices_attributes('xyz', keys=vertices)
normals = [cablenet.vertex_normal(key) for key in vertices]


bottom = points[:]
top = []
for point, normal in zip(points, normals):
    xyz = add_vectors(point, scale_vector(normal, OFFSET))
    top.append(xyz)

block = Mesh.from_vertices_and_faces(bottom + top, [[0, 3, 2, 1], [4, 5, 6, 7],
                                                    [0, 1, 5, 4], [2, 6, 5, 1],
                                                    [6, 2, 3, 7], [0, 4, 7, 3]])


# ==============================================================================
# Visualize
# ==============================================================================


artist = MeshArtist(block, layer="Boxes:Test")
artist.clear_layer()
artist.draw_faces(join_faces=True, color=(0, 255, 255))
artist.draw_vertexlabels()



