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

def draw_object(filename):
    vertices, faces = parseObj(filename)

    width = 1024
    height = 1024
    scale = 100

    image = np.full((height, width, 3), 255, dtype = np.uint8)

    rx, ry, rz = 0, 180, 0
    tx, ty, tz = 0, -3, 2
    transformed_vertices = get_rotation_matrix(vertices, rx, ry, rz, tx, ty, tz)

    ax, ay = 750, 750
    u0 = width//2
    v0 = width//2
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
    
    z_buffer = np.full((width, height), np.inf)

    for face in faces:
        dot1 = transformed_vertices[face[0]]
        dot2 = transformed_vertices[face[1]]
        dot3 = transformed_vertices[face[2]]
        
        flat_dot1 = pixel_vertices[face[0]]
        flat_dot2 = pixel_vertices[face[1]]
        flat_dot3 = pixel_vertices[face[2]]
        draw_triangle(image, dot1, dot2, dot3, z_buffer, flat_dot1, flat_dot2, flat_dot3)

    return image

def main():
    obj_filename = "Monkey.obj"
    result_image = draw_object(obj_filename)

    image = Image.fromarray(result_image)
    image = ImageOps.flip(image)
    image.show()

if __name__=="__main__":
    main()