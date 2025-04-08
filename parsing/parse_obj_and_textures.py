def parseObj(filename, scale_model):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v') and not line.startswith('vt'):
                parts = line.strip().split()[1:]
                x, y, z = map(lambda elem : float(elem)*scale_model, parts)
                vertices.append((x, y, z))
            elif line.startswith('f'):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx = part.split("/")[0]
                    face.append(int(idx)-1)
                # print(face)
                faces.append(face)
    return vertices, faces

def parse_texture(filename):
    vertice_texture = []
    faces_texture = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("vt"):
                parts = line.strip().split()[1:]
                if len(parts) == 2:
                    x, y = map(float, parts)
                    vertice_texture.append((x, y))
                else:
                    x, y, z = map(float, parts)
                    vertice_texture.append((x, y, z))
            elif line.startswith("f"):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx_texture = part.split("/")[1]
                    face.append(int(idx_texture)-1)
                # print(face)
                faces_texture.append(face)
    return faces_texture, vertice_texture