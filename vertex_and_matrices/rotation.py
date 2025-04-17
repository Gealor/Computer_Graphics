import numpy as np

def quaternion_from_angle(axis, angle):
    angle_rad = np.radians(angle)
    axis = np.array(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    w = np.cos(angle_rad/2)
    xyz = axis * np.sin(angle_rad/2)
    return np.array([w, *xyz])

def get_transform_model(vertices, axis, angle, tx, ty, tz):

    q = quaternion_from_angle(axis, angle)
    q = q / np.linalg.norm(q)

    def quat_conjugate(q):
        w, i, j, k = q
        return np.array([w, -i, -j, -k])
    
    def mult_quat(q1, q2):
        w1, i1, j1, k1 = q1
        w2, i2, j2, k2 = q2
        return np.array([
            w1*w2 - i1*i2 - j1*j2 - k1*k2,
            w1*i2 + i1*w2 + j1*k2 - k1*j2,
            w1*j2 - i1*k2 + j1*w2 + k1*i2,
            w1*k2 + i1*j2 - j1*i2 + k1*w2,
        ])
    
    def rotate_vector_with_quat(vector, quaternion):
        qv = np.array([0.0, *vector])
        q_conj = quat_conjugate(quaternion)
        return mult_quat(mult_quat(quaternion, qv), q_conj)[1:]
    
    translation = np.array([tx, ty, tz])

    transformed_vertices = []
    for vertice in vertices:
        v = np.array(vertice)
        v_rotated = rotate_vector_with_quat(v, q)
        v_transformed = v_rotated + translation
        transformed_vertices.append(tuple(v_transformed))

    return transformed_vertices