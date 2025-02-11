import math
import numpy as np
from PIL import Image
from writeLines import bresenham_line, dotted_line, dotted_line_v2, x_loop_line, x_loop_line_hotfix_1, x_loop_line_hotfix_2, x_loop_line_v2, x_loop_line_v2_no_y_calc, x_loop_line_v2_no_y_calc_v2_for_some_unknown_reason

def main():
    width, height = 512, 512

    image = np.full((width, height, 3), 255, dtype = np.uint8)

    center_x = width // 2
    center_y = height // 2

    num_arms = 13
    arm_length = 200
    dots = 200
    color = (0, 0, 255)
    for i in range(num_arms):
        angle = 2 * math.pi * i / num_arms
        end_x = center_x + arm_length * math.cos(angle)
        end_y = center_y + arm_length * math.sin(angle)
        # dotted_line(image, center_x, center_y, end_x, end_y, dots, color)
        # dotted_line_v2(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line_hotfix_1(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line_hotfix_2(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line_v2(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line_v2_no_y_calc(image, center_x, center_y, end_x, end_y, color)
        # x_loop_line_v2_no_y_calc_v2_for_some_unknown_reason(image, center_x, center_y, end_x, end_y, color)
        bresenham_line(image, center_x, center_y, end_x, end_y, color)

    img = Image.fromarray(image)
    img.show()


if __name__=="__main__":
    main()