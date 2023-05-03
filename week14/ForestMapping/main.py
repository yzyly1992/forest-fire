import argparse
import os
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # ForestMapping project root directory
# YOLOV5 = os.environ['YOLOV5_PATH']
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
# if str(YOLOV5) not in sys.path:
#     sys.path.append(str(YOLOV5))  # add yolov5 to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# from detect import run as run_yolov5
from Resize import Resize
from Merge import Merge
from ColourMap import ColourMap


def main(
        images_path=ROOT / 'images',  # folder of source images
        resized_path=ROOT / 'resized',  # folder of resized images
        noresized=False,  # do not save generated resized images
        labels_path=ROOT / 'yolov5/runs/detect/exp/labels',  # folder of files of yolov5 detected bounding boxes
        visualize_path=ROOT / 'visualize',  # folder of visualization images
        novisualize=False,  # do not generate visualization images
        out_path=ROOT / 'out',  # folder of output images and labels
        noout=False,  # do not save images to out folder
        noimages=False,  # do not save or generate any images output (set all --noresized, --novisualize, and --noout to True)
        distance=0.1,  # merging distance threshold (in pixels, 0.1 => 0 distance)
        weights=ROOT / 'weights/final_2_best.pt',  # model weight path(s)
        model_type='risks', # Current supported types: "rails" or "forest_fire"
):
    """
    python main.py \
                  --source ./images \
                  --resized ./resized \
                  --noresized \
                  --labels ./yolov5/runs/detect/exp/labels \
                  --visualize ./visualize \
                  --novisualize \
                  --out ./out \
                  --noout \
                  --noimages \
                  --distance 0.1 \
                  --weights weights/final_2_best.pt \
                  --model_type rails
    """

    # # 1. Resize images
    # print("\nResizing images...")
    # if not os.path.exists(resized_path):
    #     os.mkdir(resized_path)
    # resizer = Resize(images_path, resized_path)
    # resizer.resize()

    # # 2. Detecting bounding boxes
    # print("\nDetecting on images with yolov5...")
    # if not os.path.exists(visualize_path):
    #     os.mkdir(visualize_path)
    # if not os.path.exists(out_path):
    #     os.mkdir(out_path)
    # imgsz = (640, 640)
    # conf_thres = 0.1
    # save_txt = True
    # save_conf = True
    # nosave = True
    # exist_ok = True
    # run_yolov5(
    #     weights=weights,
    #     imgsz=imgsz,
    #     conf_thres=conf_thres,
    #     source=resized_path,
    #     save_txt=save_txt,
    #     save_conf=save_conf,
    #     nosave=nosave,
    #     exist_ok=exist_ok,
    #     project=labels_path
    # )
    full_labels_path = os.path.join(labels_path, 'exp', 'labels')
    # if noresized or noimages:
    #     resizer.remove_resized()
    #     print(f"\nAll resized images from \"{resized_path}\" removed.")

    # 3. Merge bounding boxes & colour mapping
    print("\nMerging bounding boxes...")
    novisualize = novisualize or noimages
    merger = Merge(images_path, labels_path, visualize_path, out_path, novisualize, model_type, distance)
    merger.read_images()
    imgs_merged_boxes = merger.merge()

    # Colour mapping of the merged bounding boxes
    if not (noout or noimages):
        print("\nMapping bounding boxes...")
        mapper = ColourMap(images_path, full_labels_path, out_path, imgs_merged_boxes)
        mapper.read_images()
        mapper.colour_map()
    # Save merged bounding boxes to a file
    print("\nSaving merged bounding boxes...")
    merger.save_merged_boxes()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to detect, merge, & map trees from images')
    parser.add_argument('--images-path', '--source', type=str, default='images', help='folder of source images')
    parser.add_argument('--resized-path', '--resized', type=str, default='resized', help='folder of resized images')
    parser.add_argument('--noresized', action='store_true', help='do not save generated resized images')
    parser.add_argument('--labels-path', '--labels', type=str, default='yolov5/runs/detect/exp/labels',
                        help='folder of files of yolov5 detected bounding boxes')
    parser.add_argument('--visualize-path', '--visualize', '--vis', type=str, default='visualize',
                        help='folder of visualization images')
    parser.add_argument('--novisualize', action='store_true', help='do not generate visualization images')
    parser.add_argument('--out-path', '--out', type=str, default='out', help='folder of output images and labels')
    parser.add_argument('--noout', action='store_true', help='do not save images to out folder')
    parser.add_argument('--noimages', action='store_true',
                        help='do not save or generate any images output (set all --noresized, --novisualize, and --noout to True)')
    parser.add_argument('--distance', '--dist', '--eps', type=float, default=50,
                        help='merging distance threshold (in pixels, 0.1 => 0 distance)')
    parser.add_argument('--weights', type=str, default='weights/final_2_best.pt', help='model weight path(s)')
    parser.add_argument('--model-type', type=str, default='risks', help='Current supported types: "rails" or "forest_fire"')
    args = parser.parse_args()

    main(**vars(args))
