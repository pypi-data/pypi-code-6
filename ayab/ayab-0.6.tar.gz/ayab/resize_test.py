from PIL import Image
import sys

img = Image.open("stirnband.png")
width, height = img.size

val1, val2 = 2, 4

img2 = img.transform((val1 * width, val2 * height), Image.AFFINE,
                    (1./val1, 0, 0, 0, 1./val2, 0), Image.NEAREST)

img2.save("stirn_transform.png")
