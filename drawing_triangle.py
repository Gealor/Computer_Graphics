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

def draw_triangle(image, x0, y0, z0, x1, y1, z1, x2, y2, z2, z_buffer):
    normal = compute_normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    # print(normal) if normal[2] < 0 else None
    if normal is None:
        return
    
    light_dir = np.array([0, 0, 1])
    cos_theta = np.dot(normal, light_dir) / (np.linalg.norm(normal) * np.linalg.norm(light_dir))
    # print(cos_theta)

    if cos_theta >= 0:
        return 
    
    height, width, = image.shape[:2]
    
    xmin = max(0, int(min(x0, x1, x2)))
    xmax = min(width - 1, int(max(x0, x1, x2)))
    ymin = max(0, int(min(y0, y1, y2)))
    ymax = min(height - 1, int(max(y0, y1, y2)))

    denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return 
    
    color = (-255 * cos_theta, 0, 0)
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            l1, l2, l3 = barycentric_coordinates(x, y, x0, y0, x1, y1, x2, y2)
            if l1>=0 and l2>=0 and l3>=0:
                curr_z = l1*z0 + l2*z1 + l3*z2
                if curr_z > z_buffer[y, x]:
                    continue
                else:
                    z_buffer[y, x] = curr_z
                    image[y, x] = color
                    



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


