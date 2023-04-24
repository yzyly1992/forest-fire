import os
import cv2

from ai_classes_list import get_keys


def read_images(images_path) -> dict:
    imgs = dict()  # including all original size images
    imgs_names = os.listdir(images_path)
    print(f"A total of {len(imgs_names)} images to be read.")

    for fname in sorted(imgs_names):
        if fname.lower().split(".")[-1] not in ["jpg", "jpeg", "png"]:
            print(f"Skipping file \"{fname}\"")
            continue
        img = cv2.imread(os.path.join(images_path, fname))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgs[fname] = img

    print(f"{len(imgs)} images read.")
    return imgs


def box_xywh2xyxy_v3(img_shape, boxes_xywhc):
    """
    Convert box format from yolov5 exported xywh [x, y, w, h]
      to xyxy (top-left & bottom-right coordinates [x1, y1, x2, y2])
    In-place conversion.
    """
    height, width, _ = img_shape
    for cls, boxes_cls in boxes_xywhc.items():  # for each class
        for box_id, box_xywhc in enumerate(boxes_cls):  # for each box
            cx, cy = int(width * box_xywhc[0]), int(height * box_xywhc[1])
            w, h = int(width * box_xywhc[2]), int(height * box_xywhc[3])
            conf = box_xywhc[4]
            tl = (int(cx - w / 2), int(cy - h / 2))
            br = (int(cx + w / 2), int(cy + h / 2))
            boxes_xywhc[cls][box_id] = [tl[0], tl[1], br[0], br[1], conf]
    return boxes_xywhc


def read_img_boxes_v3(fpath, img_shape, model_type = 'risks'):
    '''
    Read bboxes from 1 image + convert to xyxy format
    '''
    class_dict = get_keys()
    boxes_xywhc = {x: [] for x in class_dict[model_type]}

    with open(fpath) as f:
        for line in f:
            strs = line.strip("\n").split(" ")
            try:
                key = class_dict[model_type][int(strs[0])]
            except:
                key = 'undefined'
            boxes_xywhc[key].append([float(strs[1]), float(strs[2]), float(strs[3]), float(strs[4]), float(strs[5])])

    boxes = box_xywh2xyxy_v3(img_shape, boxes_xywhc)
    return boxes


def read_bboxes(labels_path, imgs, model_type = 'risks') -> dict:
    imgs_boxes = dict()  # including all boxes from all images
    '''
    Array format v3:
    {'image1.jpg':
        {'alive trees':
            [
                [ # box0
                    x1, y1, x2, y2, conf
                ],
                [ # box1
                    x1, y1, x2, y2, conf
                ],
                ...
            ],
        'dead trees':
            [ 
                [ # box0
                    x1, y1, x2, y2, conf
                ],
                [ # box1
                    x1, y1, x2, y2, conf
                ],
                ...
            ]
        },
    'image2.jpg':
        {'alive trees':
            [
                [ # box0
                    x1, y1, x2, y2, conf
                ],
                [ # box1
                    x1, y1, x2, y2, conf
                ],
                ...
            ],
        'dead trees':
            [ 
                [ # box0
                    x1, y1, x2, y2, conf
                ],
                [ # box1
                    x1, y1, x2, y2, conf
                ],
                ...
            ]
        },
    ...
    }
    '''

    # read boxes per image
    for fname in sorted(os.listdir(labels_path)):
        if not fname[-4:] == ".txt":
            continue
        img_name = fname[:].split('.txt')[0] + ".jpg" # `fname`: resized_raster-0-0_10.txt'
        boxes = read_img_boxes_v3(os.path.join(labels_path, fname), imgs[img_name].shape, model_type)
        imgs_boxes[img_name] = boxes
    return imgs_boxes
