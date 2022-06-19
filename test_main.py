import sys
from PIL import Image

img = Image.open(sys.argv[1])
pix = img.load()
lent, hig = img.size
print(lent, hig)