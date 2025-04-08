from PIL import Image, ImageOps
import numpy as np
from random import randint

from draw_polygons import draw_polygon
from drawing_triangle import draw_triangle
from parsing.parse_obj_and_textures import (
    parse_texture, 
    parseObj,
)
from vertex_and_matrices.rotation import get_rotation_matrix
from vertex_and_matrices.compute_vectors import (
    compute_vertex_normals,
    compute_light_intensivity,
)

def draw_object(image, width : int, height : int, scale_image : int, scale_model : int, filename_obj, texture_img, axis, angle, transfer, z_buffer):
    vertices, faces = parseObj(filename_obj, scale_model)
    try:
        texture_faces, vertices_texture = parse_texture(filename_obj)
    except:
        texture_faces, vertices_texture = [], []

    tx, ty, tz = transfer
    transformed_vertices = get_rotation_matrix(vertices, axis, angle, tx, ty, tz)

    vertices_normals = compute_vertex_normals(vertices, faces, transformed_vertices)

    ax, ay = scale_image, scale_image
    u0 = width//2
    v0 = height//2
    pixel_vertices = []
    for vertice in transformed_vertices:
        X, Y, Z = vertice
        u = ax*X/(Z+tz) + u0
        v = ay*Y/(Z+tz) + v0
        pixel_vertices.append((u, v, 1))

    for face_idx, face in enumerate(faces):
        dots = tuple(transformed_vertices[i] for i in face)
    
        flat_dots = tuple(pixel_vertices[i] for i in face)

        normal1, normal2, normal3 = vertices_normals[face[0]], vertices_normals[face[1]], vertices_normals[face[2]]

        tex_idx_face = texture_faces[face_idx]
        textures = tuple(vertices_texture[i] for i in tex_idx_face)

        avg_x = dots[0][0] + dots[1][0] + dots[2][0]
        avg_y = dots[0][1] + dots[1][1] + dots[2][1]
        avg_z = dots[0][2] + dots[1][2] + dots[2][2]
        light_dir = np.array([avg_x, avg_y, avg_z])

        intensivity_vector = compute_light_intensivity(normal1, normal2, normal3, light_dir)

        draw_polygon(image, texture_img, z_buffer, dots, flat_dots, intensivity_vector, light_dir, textures)

    return image

def main():
    obj_filename = "models/12268_banjofrog_v1_L3.obj"
    texture_name = "textures/12268_banjofrog_diffuse.jpg"
    # texture_name = "dfgbn"
    try:
        texture_img = Image.open(texture_name).convert("RGB")
        texture_img = ImageOps.flip(texture_img)
    except FileNotFoundError:
        texture_img = None

    scale_image = 1000
    scale_model = 2
    # scale_image = 35000 for rabbit
    width = 1024
    height = 600

    axis = [0.5, 0.5, 0]
    angle = 180
    transfer = [5, -5, 10]
    z_buffer = np.full((height, width), np.inf)

    image = np.full((height, width, 3), 255, dtype = np.uint8)

    for _ in range(1):
        result_image = draw_object(image, width, height, scale_image, scale_model, obj_filename, texture_img, axis, angle, transfer, z_buffer)
        transfer[2] += 2
        transfer[1] += 0.110
    image = Image.fromarray(result_image)
    image = ImageOps.flip(image)
    image.show()
    image.save("model.png")
if __name__=="__main__":
    main()