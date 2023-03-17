import numpy as np


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def rect_distance_v2(r1, r2):
    """
    Calculate distance between TWO rectangles
    Ref: https://stackoverflow.com/a/26178015/11954837
    """
    (x1, y1, x1b, y1b, _) = r1
    (x2, y2, x2b, y2b, _) = r2
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return dist((x1, y1b), (x2b, y2))
    elif left and bottom:
        return dist((x1, y1), (x2b, y2b))
    elif bottom and right:
        return dist((x1b, y1), (x2, y2b))
    elif right and top:
        return dist((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:  # rectangles intersect
        return 0.


def extract_4_vertices_rect(box):
    points = []
    points.append([box[0], box[1]])
    points.append([box[0], box[3]])
    points.append([box[2], box[3]])
    points.append([box[2], box[1]])
    return points