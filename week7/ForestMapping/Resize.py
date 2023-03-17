import os
import glob
import cv2


class Resize:
    def __init__(self, images_path, resized_path):
        self.images_path = images_path
        self.resized_path = resized_path

    def resize(self):
        imgs = []  # including all original size images
        dim = (640, 640)
        imgs_names = os.listdir(self.images_path)
        print(f"A total of {len(imgs_names)} images from \"{self.images_path}\" will be resized.")

        for fname in sorted(imgs_names):
            if fname.lower().split(".")[-1] not in ["jpg", "jpeg", "png"]:
                print(f"Skipping file \"{fname}\"")
                continue
            img = cv2.imread(os.path.join(self.images_path, fname))
            imgs.append(img)
            img_resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(self.resized_path, f"resized_{fname}"), img_resized)

        print(f"Resized images are saved in the folder \"{self.resized_path}\".")

    def remove_resized(self):
        files = glob.glob(os.path.join(self.resized_path, '*'))
        for f in files:
            os.remove(f)