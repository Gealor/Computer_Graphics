import numpy as np
from PIL import Image

from for_polygons.instruments_for_polygons import get_size_window, texturing_pixel
from vertex_and_matrices.compute_vectors import compute_normal, barycentric_coordinates

def draw_triangle(image, texture_img, z_buffer, dots, flat_dots, intensive_vector, light_dir, textures):
    
    height, width, = image.shape[:2]
    
    if texture_img:
        tex_size = texture_img.size
    
    xmin, xmax, ymin, ymax = get_size_window(width, height, flat_dots[0], flat_dots[1], flat_dots[2])
    
    # denominator = (flat_dot1[0] - flat_dot3[0]) * (flat_dot2[1] - flat_dot3[1]) - (flat_dot2[0] - flat_dot3[0]) * (flat_dot1[1] - flat_dot3[1])
    # # denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    # if abs(denominator) < 1e-10:
    #     return 
    
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):   
            l = barycentric_coordinates(x, y, flat_dots[0][0], flat_dots[0][1], flat_dots[1][0], flat_dots[1][1], flat_dots[2][0], flat_dots[2][1])
            if l[0]>=0 and l[1]>=0 and l[2]>=0:
                curr_z = l[0]*dots[0][2] + l[1]*dots[1][2] + l[2]*dots[2][2]
                if curr_z > z_buffer[y, x]:
                    continue
                else:
                    shade = -(l[0]*intensive_vector[0] + l[1]*intensive_vector[1] + l[2]*intensive_vector[2])
                    if texture_img:
                        tex_x, tex_y = texturing_pixel(z_buffer, x, y, curr_z, textures[0], textures[1], textures[2], l, tex_size)
                        tex_color = texture_img.getpixel((tex_x, tex_y))
                    else: 
                        tex_color = (255*shade, 255*shade, 255*shade)
                        z_buffer[y, x] = curr_z
    
                    final_color = shade * np.array(tex_color)
                    image[y, x] = final_color
                    # image[y, x] = color
            



