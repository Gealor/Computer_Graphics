import numpy as np

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
        vertex_normals[i] = np.array(vertex_normals[i]) / norm
    return vertex_normals

def compute_normal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    v1 = np.array([x1 - x2, y1 - y2, z1 - z2])
    v2 = np.array([x1 - x0, y1 - y0, z1 - z0])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)

def barycentric_coordinates(x, y, x0, y0, x1, y1, x2, y2): 
    denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return None
    
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / denominator
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / denominator
    lambda2 = 1.0 - lambda0 - lambda1

    return lambda0, lambda1, lambda2

def compute_light_intensivity(normal0, normal1, normal2, light_direction : np.array):
    intensivity0 = np.dot(light_direction, normal0) / (np.linalg.norm(light_direction) * np.linalg.norm(normal0))
    intensivity1 = np.dot(light_direction, normal1) / (np.linalg.norm(light_direction) * np.linalg.norm(normal1))
    intensivity2 = np.dot(light_direction, normal2) / (np.linalg.norm(light_direction) * np.linalg.norm(normal2))
    return intensivity0, intensivity1, intensivity2