# Author: Guohao Wang
# this a python script to run the SAM model with a text prompt
# it make an obvious segmentation of the image 
# You can change the text prompt to get different results on your image

# the package used in this script is samgeo
# it should be installed before running this script
from samgeo import tms_to_geotiff
from samgeo.text_sam import LangSAM

# import the SAM model
sam = LangSAM()

# text_prompt changing here
# text_prompt = "satellite, house, remote imagery"
#text_prompt = "house, remote imagery"
text_prompt = "remote imagery"

# import figure
image = 'zibo2.jpg'

# model prediction
sam.predict(image, text_prompt, box_threshold=0.24, text_threshold=0.24)

# show the image
sam.show_anns(
    cmap="Greens",
    box_color="red",
    title="Automatic Segmentation of Buildings",
    blend=True,
)

# color setting
sam.show_anns(
    cmap="OrRd_r",
    add_boxes=False,
    alpha=0.5,
    title="Segmentation of Apartment",
)

sam.show_anns(
    cmap="Greys_r",
    add_boxes=False,
    alpha=1,
    title="Automatic Segmentation",
    blend=False,
)