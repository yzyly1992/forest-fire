import os
import cv2
import numpy as np

from my_utils.drawing_functions import draw_polygon


def write_merging_results(images_path, visualize_path, imgs, imgs_merged_boxes):
    """
    Visualized merging results export to folder

    :param images_path:
    :param visualize_path:
    :param imgs:
    :param imgs_merged_boxes:
    :return:
    """
    # visualize merging result
    fnames = os.listdir(images_path)
    for img_name, img in imgs.items():  # per image
        if img_name not in imgs_merged_boxes.keys():
            continue
        for cls, poly_boxes_cls in imgs_merged_boxes[img_name].items():  # per class
            for poly_box in poly_boxes_cls:  # per box (polygon)
                img = draw_polygon(img, cls, np.array([poly_box]))
        cv2.imwrite(os.path.join(visualize_path, f"merge_vis_{img_name}"), cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
