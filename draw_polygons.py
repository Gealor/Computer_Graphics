from drawing_triangle import draw_triangle


def draw_polygon(image, texture_img, z_buffer, dots, flat_dots, intensive_vector, light_dir, textures):
    if len(dots)==3:
        draw_triangle(image, texture_img, z_buffer, dots, flat_dots, intensive_vector, light_dir, textures)
    
    else:
        for i in range(1, len(dots)-1):
            dots_ = dots[0], dots[i], dots[i+1]
            flat_dots_ = flat_dots[0], flat_dots[i], flat_dots[i+1]
            textures_ = textures[0], textures[i], textures[i+1]
            draw_triangle(image, texture_img, z_buffer, dots_, flat_dots_, intensive_vector, light_dir, textures_)
    