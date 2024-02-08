from pycocotools.coco import COCO
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Paths
annotations_path = 'base_images/updated_train.json'  # COCO annotations JSON file
images_dir = 'base_images'  # Directory containing the images
output_dir = 'label_viewing'  # Directory to save annotated images

# Initialize COCO object
coco = COCO(annotations_path)

# Get all image ids
image_ids = coco.getImgIds()

for i ,image_id in enumerate(image_ids):
    # Load image info
    image_info = coco.loadImgs(image_id)[0]
    
    # Open the image
    image_path = os.path.join(images_dir, image_info['file_name'])
    image = Image.open(image_path).convert('RGB')
    
    # Create a figure and axis for plotting
    plt.figure()
    plt.axis('off')
    plt.imshow(image)

    # Load and display instance annotations
    annIds = coco.getAnnIds(imgIds=image_info['id'], iscrowd=None)
    anns = coco.loadAnns(annIds)
    
    # Display segmentation polygons and bounding boxes
    for ann in anns:
        if 'segmentation' in ann:
            for segmentation in ann['segmentation']:
                poly = np.array(segmentation).reshape((int(len(segmentation)/2), 2))
                plt.plot(poly[:, 0], poly[:, 1], 'r', linewidth=2)
        if 'bbox' in ann:
            bbox = ann['bbox']
            plt.gca().add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
                                              fill=False, edgecolor='r', linewidth=2))

    # Save the figure directly without using PIL to avoid the temporary file
    output_path = os.path.join(output_dir, image_info['file_name'])
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()