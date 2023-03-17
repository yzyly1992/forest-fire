import cv2

from my_utils.colours import get_colour


def draw_box(img, cls, box, alpha=1.):
    """
    Overlay ONE bounding box on images with highlight option
    """
    assert alpha >= 0 and alpha <= 1, "Alpha must be between 0 and 1"
    if alpha == 1:
        img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), get_colour(cls), 5)
    else:
        img_layer = cv2.rectangle(img.copy(), (0, 0), (img.shape[1] - 1, img.shape[0] - 1), get_colour(cls),
                                  thickness=-1, lineType=cv2.LINE_AA)
        img = cv2.addWeighted(img_layer, alpha, img.copy(), 1 - alpha, 0)
    return img


def draw_polygon(img, cls, points, alpha=1.):
    assert alpha >= 0 and alpha <= 1, "Alpha must be between 0 and 1"
    if alpha == 1:
        img = cv2.polylines(img, points, True, get_colour(cls), 10)
    else:
        img_layer = cv2.fillPoly(img.copy(), points, get_colour(cls))
        img = cv2.addWeighted(img_layer, alpha, img.copy(), 1 - alpha, 0)
    return img
