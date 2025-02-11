from PIL import Image, ImageOps
import numpy as np
from writeLines import bresenham_line


def parseObj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v'):
                parts = line.strip().split()[1:]
                x, y, _ = map(float, parts)
                vertices.append((x, y))
            elif line.startswith('f'):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx = part.split("//")[0]
                    face.append(int(idx)-1)
                faces.append(face)
    return vertices, faces

def draw_object(filename):
    vertices, faces = parseObj(filename)

    width = 720
    height = 720

    scale = 60

    image = np.full((height, width, 3), 255, dtype = np.uint8)
    color = (0, 0, 255)

    pixel_vertices =[]
    for vertice in vertices:
        px, py = vertice[0]*scale + width // 2, vertice[1]*scale + height // 2
        pixel_vertices.append((px, py))
        image[int(py), int(px)] = color
    
    for face in faces:
        n = len(face)
        for i in range(n):
            start_index = face[i]
            end_index = face[(i+1) % n]

            p0 = pixel_vertices[start_index]
            p1 = pixel_vertices[end_index]
            bresenham_line(image, p0[0], p0[1], p1[0], p1[1], color)
    
    return image

def main():
    obj_filename = "Monkey.obj"
    result_image = draw_object(obj_filename)

    image = Image.fromarray(result_image)
    image = ImageOps.flip(image)
    image.show()

if __name__=="__main__":
    main()

