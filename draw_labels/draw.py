import cv2
import math
import numpy as np

from .points import sort_left, get_midpoint, project_point, get_rotated_rect, perpendicular_point
from .text import draw_text
from .utils import get_coords

# colors
WHITE = (255, 255, 255)
BLUE = (193, 87, 21)
YELLOW = (66, 185, 244)

def draw_edge(image, edge, color, point_radius=10, edge_thickness=2):
    """Draw edge on image. 
    Args:
        image: image array as opened by cv2
        edge: list of points [p0, p1], where each point is np.array in format [x, y]
        color: 
        point_radius: 
        edge_thickness:
    """
    # draw edge
    p0, p1 = sort_left(edge)
    cv2.circle(image, tuple(p0), point_radius, color, -1, lineType=cv2.LINE_AA)
    cv2.circle(image, tuple(p1), point_radius, color, -1, lineType=cv2.LINE_AA)
    cv2.line(image, tuple(p0), tuple(p1), color, edge_thickness, lineType=cv2.LINE_AA )
    return image


def draw_rounded_rect(image, color, center, theta=0, b=22, w=70):
    """Draw a rounded rect on image
    Args:
        image: image as opened by cv2
        color: 
        center: coord of center of rect, np.array in [x, y] format
        theta: angle of rotation, in radians, counter-clockwise. 
        b: distance from center to top edge of rectangle, or height / 2
        w: distance from center to left edge of rectangle, or width / 2
    """
    rect = get_rotated_rect(center, theta, b, w)
    pts = rect.reshape((-1,1,2))
    cv2.fillPoly(image, [pts], color, lineType=cv2.LINE_AA)

    # draw rounded-rect
    r0 = project_point(center, w, theta)
    r1 = project_point(center, -w, theta)
    cv2.circle(image, tuple(r0), b, color, -1, lineType=cv2.LINE_AA)
    cv2.circle(image, tuple(r1), b, color, -1, lineType=cv2.LINE_AA)
    return image


def draw_label(image, edge, text, color=YELLOW, text_color=WHITE):
    """Draw label on image. 
    Args:
        image: image as opened via cv2.
        edge: list of points [p0, p1], where each point is np.array in format [x, y]
        text: str
    """
    image = draw_edge(image, edge, color, point_radius=10, edge_thickness=2)
    # get midpoint
    c, angle = get_midpoint(edge)
    image = draw_rounded_rect(image, color, c, angle, b=22, w=70)
    # draw text
    image = draw_text(image, text, c, angle, fontScale=1, thickness=4, color=text_color)
    return image


def draw_t_label(image, points, text, color=BLUE, text_color=WHITE):
    """Draw a T-label on image. 
    For given points (p1, p2, p3) draws perpendicular edges (p1,p2), 
    and (p3,p4) where p4 is intersection of (p1,p2). Draws label on edge (p3,p4). 

    Args:
        image: image as opened via cv2. 
        points: list of points [p1,p2,p3] where each point is np.array in format [x, y]
        text: str
    """
    p1, p2, p3 = points
    edge = [p1, p2]

    image = draw_edge(image, edge, color, point_radius=10, edge_thickness=2)
    perp_point = perpendicular_point(edge[0], edge[1], p3)

    t_edge = [perp_point, p3]
    image = draw_edge(image, t_edge, color, point_radius=10, edge_thickness=2)

    # get midpoint
    c, angle = get_midpoint(t_edge, b=0.3)
    image = draw_rounded_rect(image, color, c, angle, b=22, w=70)
    # draw text
    image = draw_text(image, text, c, angle, fontScale=1, thickness=4, color=text_color)
    return image


def draw_labels(image, labels):
    """Draw labels on image. 

    Args:
        image: image opened via cv2.     
        labels: list containing [edge, text], where edge is a array of points. 
            Each point should be np.array integer coords [x, y] on image, where
            origin is image top-left. 
    """

    for label in labels:
        points = [get_coords(p) for p in label['points']]
        text = label['text']
        if len(points) > 2:
            image = draw_t_label(image, points, text)
        else:
            image = draw_label(image, points, text)
    return image