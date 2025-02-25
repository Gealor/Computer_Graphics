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


def draw_object(filename):
    vertices, faces = parseObj(filename)

    width = 1024
    height = 1024
    scale = 100

    image = np.full((height, width, 3), 255, dtype = np.uint8)

    pixel_vertices =[]
    for vertice in vertices:
        px, py, pz = vertice[0]*scale + width // 2, vertice[1]*scale + height // 2, vertice[2]*scale
        pixel_vertices.append((px, py, pz))
    
    z_buffer = np.full((width, height), np.inf)

    for face in faces:
        dot1 = pixel_vertices[face[0]]
        dot2 = pixel_vertices[face[1]]
        dot3 = pixel_vertices[face[2]]
        draw_triangle(image, dot1[0], dot1[1], dot1[2], dot2[0], dot2[1], dot2[2], dot3[0], dot3[1], dot3[2], z_buffer)

    return image

def main():
    obj_filename = "Monkey.obj"
    result_image = draw_object(obj_filename)

    image = Image.fromarray(result_image)
    image = ImageOps.flip(image)
    image.show()

if __name__=="__main__":
    main()