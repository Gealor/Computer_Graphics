def parseObj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v'):
                parts = line.strip().split('/')[1:]
                x, y, _ = map(float, parts)
                vertices.append((x, y))
            elif line.startwith('f'):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    idx = part.split("//")[0]
                    face.append(int(idx)-1)
