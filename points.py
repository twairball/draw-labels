import cv2
import math
import numpy as np


def sort_left(points):
    """sort list of points by x-axis 
    Ref:
    - https://stackoverflow.com/questions/2706605/sorting-a-2d-numpy-array-by-multiple-axes
    """
    a = np.asarray(points)
    ind = np.lexsort((a[:,1], a[:,0]))  
    return a[ind]


def get_midpoint(edge):
    """Get midpoint of an edge. Returns center point and angle of projection. """

    p0, p1 = sort_left(edge)
    c = p1 - p0
    c = p0 + c/2
    c = c.astype(np.int)
    
    # note -- y-axis is reversed p1_y - p2_y as origin is top-left in image. 
    angle = math.atan((p0[1]-p1[1])/(p1[0]-p0[0]))
    return c, angle


def project_point(point, w, theta):
    """project from point at angle theta, along distance w"""
    
    # y axis inverted because image origin is top left
    proj = np.asarray([w * math.cos(theta), -w * math.sin(theta)])
    proj += point
    proj = proj.astype(np.int)
    return proj


def get_rotated_rect(center, theta, b=22, w=70):
    """Get 4 coords of rectangle rotated around center with
    width 2 * b and length 2 * w, with rotation angle theta in radians. 
    
    References: 
    - https://math.stackexchange.com/questions/2518607/how-to-find-vertices-of-a-rectangle-when-center-coordinates-and-angle-of-tilt-is
    """
    
    xs = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
    xs = np.dot(xs, [[w * math.cos(theta)], [b * math.sin(theta)]])
    
    # note: reversed y axis since image starts at top-left 
    ys = [[1, -1], [-1, -1], [-1, 1], [1, 1]]
    ys = np.dot(ys, [[w * math.sin(theta)], [b * math.cos(theta)]])
    
    rect = np.concatenate([xs, ys], axis=1)
    rect = rect.astype(np.int)    
    rect = rect + center
    return rect
