import math
import numpy as np


def dotted_line(image, x0 : float, y0 : float, x1 : float, y1 : float, count : int, color : int): 
    step = 1.0 / count

    for t in np.arange(0, 1, step):
        x = round((1.0 - t) * x0 + t*x1)
        y = round((1.0 - t) * y0 + t*y1)
        image[y, x] = color
    

def dotted_line_v2(image, x0 : float, y0 : float, x1 : float, y1 : float, color : int): 
    count = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    step = 1.0 / count

    for t in np.arange(0, 1, step):
        x = round((1.0 - t) * x0 + t*x1)
        y = round((1.0 - t) * y0 + t*y1)
        image[y, x] = color

def x_loop_line(image, x0, y0, x1, y1, color): 
    for x in range(int(x0), int(x1)):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t*y1)
        image[y, x] = color

def x_loop_line_hotfix_1(image, x0 : float, y0 : float, x1 : float, y1 : float, color : int):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range(int(x0), int(x1)):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t*y1)
        image[y, x] = color

def x_loop_line_hotfix_2(image, x0 : float, y0 : float, x1 : float, y1 : float, color : int): 
    xchange = False
    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    for x in range(int(x0), int(x1)):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t*y1)
        if xchange:
            image[x, y] = color
        else:
            image[y, x] = color

def x_loop_line_v2(image, x0 : float, y0 : float, x1 : float, y1 : float, color : int): 
    xchange = False
    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range(int(x0), int(x1)):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t*y1)
        if xchange:
            image[x, y] = color
        else:
            image[y, x] = color

def x_loop_line_v2_no_y_calc(image, x0 : float, y0 : float, x1 : float, y1 : float, color : int): 
    xchange = False
    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dydx = abs(y1 - y0)/(x1 - x0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    for x in range(int(x0), int(x1)):
        if xchange:
            image[x, int(y)] = color
        else:
            image[int(y), x] = color
        derror += dydx
        if derror >= 0.5:
            derror -= 1
            y += y_update


def x_loop_line_v2_no_y_calc_v2_for_some_unknown_reason(image, x0 : float, y0 : float, x1 : float, y1 : float, color): 
    xchange = False
    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dydx = 2.0 * (x1 - x0) * abs(y1 - y0)/(x1 - x0) 
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    for x in range(int(x0), int(x1)):
        if xchange:
            image[x, int(y)] = color
        else:
            image[int(y), x] = color
        derror += dydx
        if derror >= 2.0 * (x1 - x0) * 0.5:
            derror -= 2.0 * (x1 - x0) * 1
            y += y_update

def bresenham_line(image, x0 : float, y0 : float, x1 : float, y1 : float, color): 
    xchange = False
    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dydx = 2 * abs(y1 - y0)
    derror = 0
    y_update = 1 if y1 > y0 else -1
    for x in range(int(x0), int(x1)):
        if xchange:
            image[x, int(y)] = color
        else:
            image[int(y), x] = color
        derror += dydx
        if derror >= (x1 - x0):
            derror -= 2 * (x1 - x0)
            y += y_update
