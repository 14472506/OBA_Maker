"""
===================================================================================================
Details
===================================================================================================
"""
# imports =========================================================================================
from tools.utils import json_loader, json_saver, ImgDataGet, img_dir_lister
import os
import random
from PIL import Image, ImageDraw

# class ===========================================================================================
class BasicOBAMaker():
    """ Detials """
    def __init__(self, cfg):
        """ Detials """
        # init from cfg
        self._cfg_extractor(cfg)
        # init local
        self.base_label_data = json_loader(os.path.join(self.base_ds_root, self.bs_json_title))
        self.backg_imgs_list = img_dir_lister(self.backg_imgs_root)
        self.new_anns = []
        self.new_imgs_info = []

    def _cfg_extractor(self, cfg):
        """ detials """
        # master cfg
        self.cfg = cfg
        # root attibures and file titles
        self.base_ds_root = cfg["roots"]["base_imgs"]
        self.gen_ds_root = cfg["roots"]["gen_imgs"]
        self.backg_imgs_root = cfg["roots"]["background"]
        self.bs_json_title = cfg["roots"]["base_json"]
        self.gen_json_title = cfg["roots"]["gen_json"]
        # generator parameters
        self.epochs = cfg["generator_params"]["epochs"]
        self.out_type = cfg["generator_params"]["out_type"]

    def run(self):
        """ detials """
        for _ in range(self.epochs):
            for image_info in self.base_label_data["images"]:
                # get individual data elements
                image_id = image_info["id"]
                base_image = ImgDataGet.get_image(os.path.join(self.base_ds_root, image_info["file_name"]), get_type="basic")
                base_width, base_height = base_image.size
                annotations = [anno for anno in self.base_label_data['annotations'] if anno['image_id'] == image_id]
                backg_image_path = os.path.join(self.backg_imgs_root, random.choice(self.backg_imgs_list))
                backg_image = ImgDataGet.get_image(backg_image_path, get_type="resize", nwidth=base_width, nheight=base_height)

                # generate and save new image
                gen_image = self._copy_instances(base_image, backg_image, annotations)
                gen_image_name = f'basic_oba_{len(self.base_label_data["images"])+len(self.new_imgs_info)}.jpg'
                gen_image.save(os.path.join(self.gen_ds_root, gen_image_name)) 

                # generate and update new image meta data
                gen_image_info = dict(image_info)
                gen_image_info["file_name"] = gen_image_name
                gen_image_info['id'] = len(self.base_label_data['images']) + len(self.new_imgs_info)
                self.new_imgs_info.append(gen_image_info) 

                for ann in annotations:
                    gen_ann = dict(ann)
                    gen_ann["image_id"] = gen_image_info["id"]
                    gen_ann["id"] = len(self.base_label_data["annotations"]) + len(self.new_anns)
                    self.new_anns.append(gen_ann)
        
        self._gen_data_saver()

    def _copy_instances(self, source_image, target_image, anns):
        """ detials """
        for ann in anns:
            for segm in ann["segmentation"]:
                mask = Image.new("L", source_image.size, 0)
                draw = ImageDraw.Draw(mask)
                try:
                    draw.polygon(segm, fill=255)
                except TypeError as e:
                    print(f"Error drawing polygone: {e}")
                    continue
                target_image.paste(source_image, (0, 0), mask)
        return target_image
    
    def _gen_data_saver(self):
        """ Detials """
        if self.out_type == "extend":
            self.base_label_data['images'].extend(self.new_imgs_info)
            self.base_label_data['annotations'].extend(self.new_anns)
        if self.out_type == "new":
            self.base_label_data['images'] = self.new_imgs_info
            self.base_label_data['annotations'] = self.new_anns
        
        json_saver(os.path.join(self.gen_ds_root, self.gen_json_title), self.base_label_data, ind_num=4)
        




