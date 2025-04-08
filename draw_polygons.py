import numpy as np
from drawing_triangle import draw_triangle
from vertex_and_matrices.compute_vectors import compute_light_intensivity, compute_normal


def draw_polygon(image, texture_img, z_buffer, dots, flat_dots, normals, light_dir, textures):
    
    normal = compute_normal(
        dots[0][0], dots[0][1], dots[0][2], 
        dots[1][0], dots[1][1], dots[1][2], 
        dots[2][0], dots[2][1], dots[2][2],
    )

    cos_theta = np.dot(normal, light_dir) / (np.linalg.norm(normal) * np.linalg.norm(light_dir))

    if cos_theta >= 0:
        return 

    if len(dots)==3:
        intensive_vector = compute_light_intensivity(normals[0], normals[1], normals[2], light_dir)
        draw_triangle(image, texture_img, z_buffer, dots, flat_dots, intensive_vector, light_dir, textures)
    
    else:
        for i in range(1, len(dots)-1):
            dots_ = dots[0], dots[i], dots[i+1]
            flat_dots_ = flat_dots[0], flat_dots[i], flat_dots[i+1]
            textures_ = textures[0], textures[i], textures[i+1]
            intensive_vector = compute_light_intensivity(normals[0], normals[i], normals[i+1], light_dir)
            
            draw_triangle(image, texture_img, z_buffer, dots_, flat_dots_, intensive_vector, light_dir, textures_)
    