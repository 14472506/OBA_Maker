"""
===================================================================================================
Detials
===================================================================================================
"""
# imports =========================================================================================
import json
from PIL import Image
import os

# classes =========================================================================================
class ImgDataGet():
    """ Detials """
    def __init__(self, path, get_type, nwidth=None, nheight=None):
        self.path = path
        self.type = get_type
        self.nwidth = nwidth
        self.nheight = nheight
        self.img = self._load_img()
        
    @classmethod
    def get_image(cls, path, get_type, nwidth=None, nheight=None):
        instance = cls(path, get_type, nwidth, nheight)
        return instance.img

    def _load_img(self):
        """ detials """
        img = Image.open(self.path)
        if self.type == "basic":
            return img
        if self.type == "resize":
            return self._image_resize(img)

    def _image_resize(self, img):
        """ Detials """
        width, height = img.size
        aspect_ratio = width/height
        new_aspect_ratio = self.nwidth/self.nheight
        if aspect_ratio != new_aspect_ratio:
            left, top, right, bottom = self._resize_aspect_dims(width, height, new_aspect_ratio)
            img = img.crop((left, top, right, bottom))
            img = img.resize((self.nwidth, self.nheight), Image.ANTIALIAS)
        return(img)

    def _resize_aspect_dims(self, width, height, aspect_ratio):
        """ Detials """
        copy_height = height
        copy_width = copy_height * aspect_ratio
        if copy_width > width:
            copy_width = width
            copy_height = copy_width / aspect_ratio
        
        left = (width - copy_width)/2
        top = (height - copy_height)/2
        right = (width + copy_width)/2
        bottom = (height + copy_height)/2

        return left, top, right, bottom

# functions =======================================================================================
def json_loader(json_dir):
    """ detials """
    with open(json_dir, "r") as file:
        return json.load(file)

def json_saver(json_dir, data, ind_num=1):
    """ Detials """
    with open(json_dir, 'w') as file:
        json.dump(data, file, indent=ind_num)

def img_dir_lister(path):
    """ detials """
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif')
    return [f for f in os.listdir(path) if f.lower().endswith(image_extensions)]