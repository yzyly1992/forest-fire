import os
import json
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull

from my_utils.file_readers import read_images, read_bboxes
from my_utils.file_writers import write_merging_results
from my_utils.rect_calculate import rect_distance_v2, extract_4_vertices_rect


class Merge:
    def __init__(self, images_path, labels_path, visualize_path, out_path, novisualize, model_type='risks', eps=0.1):
        self.images_path = images_path
        self.labels_path = labels_path
        self.visualize_path = visualize_path
        self.out_path = out_path
        self.novisualize = novisualize
        self.model_type = model_type
        self.eps = eps
        self.imgs = dict()
        self.imgs_boxes = dict()
        self.imgs_merged_boxes = dict()
        '''
        same Array format as `imgs_boxes` except dimension 3:
        [ # *dim 3*: each box
          (x1, y1), (x2, y2), ..., (xn, yn)
        ]
        '''

    def read_images(self):
        # Read images and bounding boxes
        self.imgs = read_images(self.images_path)
        self.imgs_boxes = read_bboxes(self.labels_path, self.imgs, self.model_type)
        print(f"A total of {len(self.imgs)} images are read from \"{self.images_path}\". {len(self.imgs_boxes)} "
              f"corresponding files of bounding boxes info are read from \"{self.labels_path}\".")

    def merge_boxes_hull(self, boxes):
        points = []
        for box in boxes:
            points.append([box[0], box[1]])
            points.append([box[0], box[3]])
            points.append([box[2], box[3]])
            points.append([box[2], box[1]])
        hull = ConvexHull(points)
        hull_points = [points[id] for id in hull.vertices]
        return hull_points

    def merge_boxes_rect(self, r1, r2):
        """
        Merge TWO rectangle bounding boxes --into--> ONE rectangle bounding box
        """
        (x1, y1, x1b, y1b) = r1
        (x2, y2, x2b, y2b) = r2
        tl_x = min(x1, x2)
        tl_y = min(y1, y2)
        br_x = max(x1b, x2b)
        br_y = max(y1b, y2b)
        return (tl_x, tl_y, br_x, br_y)

    def merge(self):
        """
        :param images_path:
        :param labels_path:
        :param visualize_path:
        :param eps: defined pixel distance threshold
        :return:
        """
        assert len(self.imgs_boxes) != 0, "Please read images and bounding boxes first. Or no detected objects " \
                                          "across all images."

        # Merge bounding boxes - with algorithms
        for img_name, boxes in self.imgs_boxes.items():  # per image
            new_boxes = {}
            for cls, boxes_cls in boxes.items():  # per class
                # Empty class handling
                if len(boxes_cls) == 0:
                    new_boxes[cls] = []
                    continue

                # DBSCAN - algorithm to merge boxes
                """
                eps: distance in pixels to merge (0.1 to merge intersected boxes)
                min_samples: minimum 2 boxes can merge together
                metric: distance function (defined `rect_distance`)
                """
                result = DBSCAN(eps=self.eps, min_samples=2, metric=rect_distance_v2).fit(boxes_cls)
                # print(result.labels_)

                # Create ONE new box per merged boxes
                new_boxes_cls = []
                clusters = {cls: [] for cls in set(result.labels_) if
                            cls != -1}  # group boxes with same class in dictionary
                for id, cls_id in enumerate(result.labels_):  # add all single (class==-1) boxes
                    if cls_id == -1:
                        new_boxes_cls.append(extract_4_vertices_rect(boxes_cls[id]))
                    else:
                        clusters[cls_id].append(boxes_cls[id])
                for key, val in clusters.items():
                    # merge to convexhull
                    box_res = self.merge_boxes_hull(val)

                    new_boxes_cls.append(box_res)
                new_boxes[cls] = new_boxes_cls
            self.imgs_merged_boxes[img_name] = new_boxes  # append all merged boxes per image

        # Visualizations save to folder
        if not self.novisualize:
            write_merging_results(self.images_path, self.visualize_path, self.imgs, self.imgs_merged_boxes)
            print(f"Merged boxes' visualizations saved to \"{self.visualize_path}\"")
        print("`imgs_merged_boxes` variable returned.")

        return self.imgs_merged_boxes

    def save_merged_boxes(self):
        """
        Save merged boxes to file
        :return:
        """
        with open(os.path.join(self.out_path, "out_boxes.json"), "w") as outfile:
            json.dump(self.imgs_merged_boxes, outfile, indent=4, sort_keys=False)
        print(f"Merged boxes saved as \"{os.path.join(self.out_path, 'out_boxes.json')}\"")
