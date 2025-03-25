from PIL import Image, ImageOps
import numpy as np
from random import randint

from drawing_triangle import draw_triangle


def parseObj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v') and not line.startswith('vt'):
                parts = line.strip().split()[1:]
                x, y, z = map(float, parts)
                vertices.append((x, y, z))
            elif line.startswith('f'):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx = part.split("/")[0]
                    face.append(int(idx)-1)
                faces.append(face)
    return vertices, faces

def parse_texture(filename):
    vertice_texture = []
    faces_texture = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("vt"):
                parts = line.strip().split()[1:]
                x, y = map(float, parts)
                vertice_texture.append((x,y))
            elif line.startswith("f"):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx_texture = part.split("/")[1]
                    face.append(int(idx_texture)-1)
                faces_texture.append(face)
    return faces_texture, vertice_texture

def get_rotation_matrix(vertices, px, py, pz, tx, ty, tz):

    angle_x = np.radians(px)
    angle_y = np.radians(py)
    angle_z = np.radians(pz)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    Ry = np.array([
        [np.cos(angle_y), 0, -np.sin(angle_y)],
        [0, 1, 0],
        [np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    Rz = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z),  np.cos(angle_z), 0],
        [0, 0, 1]
    ])

    R = Rx.dot(Ry).dot(Rz)

    translation = np.array([tx, ty, tz])

    transformed_vertices = []
    for vertice in vertices:
        v = np.array(vertice)
        v_transformed = R.dot(v) + translation
        transformed_vertices.append(tuple(v_transformed))

    return transformed_vertices

def compute_vertex_normals(vertices, faces, transformed_vertices):
    vertex_normals = [np.zeros(3) for _ in vertices]

    for face in faces:
        v0 = np.array(transformed_vertices[face[0]])
        v1 = np.array(transformed_vertices[face[1]])
        v2 = np.array(transformed_vertices[face[2]])

        edge1 = v1 - v0
        edge2 = v2 - v0

        normal = np.cross(edge1, edge2)
        normal /= np.linalg.norm(normal)
        for idx in face:
            vertex_normals[idx] += normal

    for i in range(len(vertex_normals)):
        norm = np.linalg.norm(vertex_normals[i])
        vertex_normals[i] /= norm
    return vertex_normals

def compute_light_intensivity(normal0, normal1, normal2, light_direction : np.array):

    intensivity0 = np.dot(light_direction, normal0) / (np.linalg.norm(light_direction) * np.linalg.norm(normal0))
    intensivity1 = np.dot(light_direction, normal1) / (np.linalg.norm(light_direction) * np.linalg.norm(normal1))
    intensivity2 = np.dot(light_direction, normal2) / (np.linalg.norm(light_direction) * np.linalg.norm(normal2))
    return intensivity0, intensivity1, intensivity2

def draw_object(image, width, height, filename, texture_img, rx, ry, rz, tx, ty, tz, z_buffer):
    vertices, faces = parseObj(filename)
    texture_faces, vertices_texture = parse_texture(filename)

    width = 1024
    height = 1024

    # rx, ry, rz = 0, 180, 0
    # tx, ty, tz = 0, -0.05, 4
    transformed_vertices = get_rotation_matrix(vertices, rx, ry, rz, tx, ty, tz)


    vertices_normals = compute_vertex_normals(vertices, faces, transformed_vertices)

    ax, ay = 35000, 35000
    u0 = width//2
    v0 = height//2
    pixel_vertices = []
    for vertice in transformed_vertices:
        X, Y, Z = vertice
        u = ax*X/(Z+tz) + u0
        v = ay*Y/(Z+tz) + v0
        pixel_vertices.append((u, v, 1))

    # pixel_vertices = []
    # for vertice in transformed_vertices:
    #     px, py, pz = vertice[0]*scale, vertice[1]*scale, vertice[2]*scale
    #     pixel_vertices.append((px, py, pz))
    
    # z_buffer = np.full((width, height), np.inf)

    for face_idx, face in enumerate(faces):
        dot1 = transformed_vertices[face[0]]
        dot2 = transformed_vertices[face[1]]
        dot3 = transformed_vertices[face[2]]
        
        flat_dot1 = pixel_vertices[face[0]]
        flat_dot2 = pixel_vertices[face[1]]
        flat_dot3 = pixel_vertices[face[2]]

        normal1 = vertices_normals[face[0]]
        normal2 = vertices_normals[face[1]]
        normal3 = vertices_normals[face[2]]

        tex_idx_face = texture_faces[face_idx]
        texture1 = vertices_texture[tex_idx_face[0]]
        texture2 = vertices_texture[tex_idx_face[1]]
        texture3 = vertices_texture[tex_idx_face[2]]

        avg_x = dot1[0] + dot2[0] + dot3[0]
        avg_y = dot1[1] + dot2[1] + dot3[1]
        avg_z = dot1[2] + dot2[2] + dot3[2]
        light_dir = np.array([avg_x+1, avg_y+1, avg_z+1])
        # light_dir = np.array([0, 0, 1])

        intensivity1, intensivity2, intensivity3 = compute_light_intensivity(normal1, normal2, normal3, light_dir)

        draw_triangle(image, z_buffer, dot1, dot2, dot3, flat_dot1, flat_dot2, flat_dot3, intensivity1, intensivity2, intensivity3, light_dir, texture1, texture2, texture3, texture_img)

    return image

def main():
    obj_filename = "model_1.obj"
    texture_name = "bunny-atlas.jpg"
    texture_img = Image.open(texture_name).convert("RGB")
    texture_img = ImageOps.flip(texture_img)

    width = 1024
    height = 1024

    rx, ry, rz = 0, 160, 0
    tx, ty, tz = 0, -0.05, 4
    z_buffer = np.full((width, height), np.inf)

    image = np.full((height, width, 3), 255, dtype = np.uint8)

    for _ in range(3):
        result_image = draw_object(image, width, height, obj_filename, texture_img, rx, ry, rz, tx, ty, tz, z_buffer)
        tz += 2
        ty += 0.1
    image = Image.fromarray(result_image)
    image = ImageOps.flip(image)
    image.show()

if __name__=="__main__":
    main()