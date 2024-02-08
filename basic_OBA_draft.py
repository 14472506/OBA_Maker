"""
===================================================================================================
basic oba draft
===================================================================================================
"""
import json
import os
import random
from PIL import Image, ImageDraw

class BasicOBA():
    """ Detials """
    def __init__(self, config):
        self.config = config
        self.backgound_img_list = self._image_list_generator(config["background_dir"])
        self.coco_data = self._json_loader(config["base_json"])
        self.base_dir = config["base_dir"]
        self.new_json = config["new_json"]
        self.background_dir = config["background_dir"]
        self.epochs = config["epochs"]
        self.new_anns = []
        self.new_imgs_info = []

    def _image_list_generator(self, background_dir):
        """ Details """
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif')
        return [f for f in os.listdir(background_dir) if f.lower().endswith(image_extensions)]
    
    def _json_loader(self, json_dir):
        """ Detials """
        with open(json_dir) as f:
            return json.load(f)
    
    def _json_saver(self, json_dir):
        """ Detials """
        with open(json_dir, 'w') as f:
            json.dump(self.coco_data, f, indent=4)
        
    def _get_image_data(self, image_path):
        """ Detials """
        # Load the original image
        image = Image.open(image_path)
        width, height = image.size
        return image, width, height
    
    def _get_background_image(self, width, height):
        """ Detials """
        background_img_root = random.choice(self.backgound_img_list)
        background_img = Image.open(os.path.join(self.background_dir, background_img_root))
        aspect_ratio = width/height

        if width < 1920:
            # Calculate the largest possible crop dimensions with a 16:9 aspect ratio
            orig_width, orig_height = background_img.size
            crop_height = orig_height
            crop_width = crop_height * aspect_ratio
            if crop_width > orig_width:
                # If the calculated width exceeds the image's width, adjust the height instead
                crop_width = orig_width
                crop_height = crop_width / aspect_ratio

            # Calculate the crop area
            left = (orig_width - crop_width) / 2
            top = (orig_height - crop_height) / 2
            right = (orig_width + crop_width) / 2
            bottom = (orig_height + crop_height) / 2

            # Crop and resize the image
            background_img = background_img.crop((left, top, right, bottom))
            background_img = background_img.resize((width, height), Image.ANTIALIAS)

        return background_img

    def _copy_instances(self, annotations, image, background_image):
        """ Detials """
        for annotation in annotations:
            for segmentation in annotation['segmentation']:
                mask = Image.new('L', image.size, 0)
                draw = ImageDraw.Draw(mask)
                try:
                    draw.polygon(segmentation, fill=255)
                except TypeError as e:
                    print(f"Error drawing polygon: {e}")
                    continue

                background_image.paste(image, (0, 0), mask)
        
        return background_image
    
    def _new_annotations(self, annotations, new_image_info):
        """ Detials """
        for annotation in annotations:
            new_annotation = dict(annotation)
            new_annotation['image_id'] = new_image_info['id']  # Update to new image ID
            new_annotation['id'] = len(self.coco_data['annotations']) + len(self.new_anns)  # Assign a new ID
            self.new_anns.append(new_annotation)
        return new_annotation
    
    def generate(self):
        """ Detials """
        for _ in range(self.epochs):
            for image_info in self.coco_data['images']:
                image_id = image_info['id']
                image_path = f"base_images/{image_info['file_name']}"
                image, width, height = self._get_image_data(image_path)
                      
                annotations = [anno for anno in self.coco_data['annotations'] if anno['image_id'] == image_id]

                background_image = self._get_background_image(width, height)
                new_image = self._copy_instances(annotations, image, background_image)

                # Save the new image
                new_image_name = f"new_{(len(self.coco_data['images']) + len(self.new_imgs_info))}.jpg"
                new_image_path = f"test_gen/{new_image_name}"
                new_image.save(new_image_path)

                # Update new_images list for JSON
                new_image_info = dict(image_info)  # Copy original image_info
                new_image_info['file_name'] = new_image_name
                new_image_info['id'] = len(self.coco_data['images']) + len(self.new_imgs_info)  # Assign a new ID
                self.new_imgs_info.append(new_image_info)

                new_annotations = self._new_annotations(annotations, new_image_info)
                # Add new images and annotations to the original data
        self.coco_data['images'].extend(self.new_imgs_info)
        self.coco_data['annotations'].extend(self.new_anns)
        
        self._json_saver(self.new_json)

if __name__ == "__main__":

    # define config
    config = {
        "base_json": "base_images/train.json", 
        "base_dir": "base_images",
        "new_json": "test_gen/oba_train.json",
        "out_dir": "test_gen",
        "background_dir": "processed_background_images",
        "epochs": 3
    }

    oba_gen = BasicOBA(config)
    oba_gen.generate()
