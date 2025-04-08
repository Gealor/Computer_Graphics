

def get_size_window(width, height, flat_dot1: list, flat_dot2: list, flat_dot3: list):
    xmin = max(0, int(min(flat_dot1[0], flat_dot2[0], flat_dot3[0])))
    xmax = min(width - 1, int(max(flat_dot1[0], flat_dot2[0], flat_dot3[0])))
    ymin = max(0, int(min(flat_dot1[1], flat_dot2[1], flat_dot3[1])))
    ymax = min(height - 1, int(max(flat_dot1[1], flat_dot2[1], flat_dot3[1])))
    return xmin, xmax, ymin, ymax


def texturing_pixel(z_buffer, x, y, curr_z, texture1: list, texture2: list, texture3: list, l: list, tex_size: list):
    z_buffer[y, x] = curr_z
    u_interp = l[0] * texture1[0] + l[1] * texture2[0] + l[2] * texture3[0]
    v_interp = l[0] * texture1[1] + l[1] * texture2[1] + l[2] * texture3[1]
    tex_x = int(round(u_interp * (tex_size[0] - 1)))
    tex_y = int(round(v_interp * (tex_size[1] - 1)))
    return tex_x, tex_y