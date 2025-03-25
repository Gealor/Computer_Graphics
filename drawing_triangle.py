import numpy as np
from PIL import Image

def barycentric_coordinates(x, y, x0, y0, x1, y1, x2, y2): 
    denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return None
    
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / denominator
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / denominator
    lambda2 = 1.0 - lambda0 - lambda1

    return lambda0, lambda1, lambda2

def compute_normal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    v1 = np.array([x1 - x2, y1 - y2, z1 - z2])
    v2 = np.array([x1 - x0, y1 - y0, z1 - z0])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)

def compute_light_intensivity(vertex_normals : np.array, light_direction : np.array):
    intesivity = []
    for normal in vertex_normals:
        intesivity = np.dot(light_direction, normal) / (np.linalg.norm(light_direction) * np.linalg.norm(normal))
        intesivity.append(intesivity)
    return intesivity

def draw_triangle(image, z_buffer, dot1, dot2, dot3, flat_dot1, flat_dot2, flat_dot3, intensive1, intensive2, intensive3, light_dir, texture1, texture2, texture3, texture_img):
    
    normal = compute_normal(dot1[0], dot1[1], dot1[2], dot2[0], dot2[1], dot2[2], dot3[0], dot3[1], dot3[2])
    # print(normal) if normal[2] < 0 else None
    if normal is None:
        return
    
    cos_theta = np.dot(normal, light_dir) / (np.linalg.norm(normal) * np.linalg.norm(light_dir))
    # print(cos_theta)

    if cos_theta >= 0:
        return 
    
    height, width, = image.shape[:2]
    tex_width, tex_height = texture_img.size
    
    xmin = max(0, int(min(flat_dot1[0], flat_dot2[0], flat_dot3[0])))
    xmax = min(width - 1, int(max(flat_dot1[0], flat_dot2[0], flat_dot3[0])))
    ymin = max(0, int(min(flat_dot1[1], flat_dot2[1], flat_dot3[1])))
    ymax = min(height - 1, int(max(flat_dot1[1], flat_dot2[1], flat_dot3[1])))
    
    denominator = (flat_dot1[0] - flat_dot3[0]) * (flat_dot2[1] - flat_dot3[1]) - (flat_dot2[0] - flat_dot3[0]) * (flat_dot1[1] - flat_dot3[1])
    # denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return 
    
    # color = (-255 * cos_theta, 0, 0)
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):   
            l1, l2, l3 = barycentric_coordinates(x, y, flat_dot1[0], flat_dot1[1], flat_dot2[0], flat_dot2[1], flat_dot3[0], flat_dot3[1])
            # color = (-255 * (l1*intensive1 + l2*intensive2 + l3*intensive3), 0, 0)
            if l1>=0 and l2>=0 and l3>=0:
                curr_z = l1*dot1[2] + l2*dot2[2] + l3*dot3[2]
                if curr_z > z_buffer[y, x]:
                    continue
                else:
                    z_buffer[y, x] = curr_z
                    u_interp = l1 * texture1[0] + l2 * texture2[0] + l3 * texture3[0]
                    v_interp = l1 * texture1[1] + l2 * texture2[1] + l3 * texture3[1]
                    tex_x = int(round(u_interp * (tex_width - 1)))
                    tex_y = int(round(v_interp * (tex_height - 1)))
                    
                    tex_color = texture_img.getpixel((tex_x, tex_y))
                    shade = -(l1*intensive1 + l2*intensive2 + l3*intensive3)
                    final_color = shade * np.array(tex_color)
                    image[y, x] = final_color
                    # image[y, x] = color
            
            

def main():
    width, height = 512, 512
    image = np.full((height, width), 255, dtype=np.uint8)
    x0, y0, z0 = 100.5, 100.5, 40.5
    x1, y1, z1 = 480.5, 420.0, 50.5
    x2, y2, z2 = 130.0, 490.0, 20.5
    color = 255
    draw_triangle(image, x0, y0, z0, x1, y1, z1, x2, y2, z2, color)
    img = Image.fromarray(image)
    img.show()

if __name__=="__main__":
    main()


