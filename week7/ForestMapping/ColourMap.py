import os
import cv2
import numpy as np

from my_utils.file_readers import read_images
from my_utils.drawing_functions import draw_box, draw_polygon
from my_utils.rect_calculate import extract_4_vertices_rect


class ColourMap:
    def __init__(self, images_path, labels_path, out_path, imgs_merged_boxes):
        self.images_path = images_path
        self.labels_path = labels_path
        self.out_path = out_path
        self.imgs_merged_boxes = imgs_merged_boxes
        self.imgs = dict()

    def read_images(self):
        # read images
        self.imgs = read_images(self.images_path)
        print(f"A total of {len(self.imgs)} images are read from \"{self.images_path}\".")

    def colour_map(self):
        assert len(self.imgs) != 0, "Please read images first."
        alpha = 0.5 # transparency of the overlay

        # map entire frame blue colour
        print(f"Start mapping each entire image with blue colour.")
        imgs_new = dict()
        for img_id, (img_name, img) in enumerate(self.imgs.items()):
            if img_id % 50 == 0:
                print(f"{img_id}/{len(self.imgs)} images are processed.")
            box = extract_4_vertices_rect([0, 0, img.shape[1], img.shape[0]])
            img2 = draw_box(img, "4", box, alpha)
            imgs_new[img_name] = img2
        self.imgs = imgs_new
        print(f"All {len(self.imgs)} images are mapped with blue colour.")

        # map each bounding box (polygon) with yellow or red colour
        print(f"Start mapping alive & dead trees in each image with colours.")
        for img_id, (img_name, img) in enumerate(self.imgs.items()):
            if img_id % 5 == 0:
                print(f"{img_id}/{len(self.imgs)} images are processed.")
            if img_name not in self.imgs_merged_boxes.keys():
                continue
            for cls, poly_boxes_cls in self.imgs_merged_boxes[img_name].items():  # per class
                for poly_box in poly_boxes_cls:  # per box (polygon)
                    img = draw_polygon(img, cls, np.array([poly_box]), alpha)
            cv2.imwrite(os.path.join(self.out_path, f"map_vis_{img_name}"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"All alive & dead trees are mapped with yellow or red colours across {len(self.imgs)} images.")

        print(f"Mapped images are saved in \"{self.out_path}\".")
