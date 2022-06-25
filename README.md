# Python Implementation of Pixel Value Differencing based Steganography

LSB substitution and PVD are applied. In PVD, adaptive non-overlapping 3x3 pixel blocks or a combination of 3x3 and 2x2 blocks are used in raster fashion.

The file `test_main.py` is an example usage of the `pvd_lib.py` PVD library. 

For encoding, the following data are required:
1. Reference PNG image 
2. Secret message as .txt file
3. Path/name of the PVD embedded image

For decoding, the following data are required:
1. Reference PNG image
2. Secret message file/path as .txt file which will be written with the secret data read from the PVD embedded image
3. Path/name of the PVD embedded image

**Only PNG Image** files should be used as cover image and final output image.

## Getting Started

Clone repository and enter the repository folder.

### Prerequisites

Requires,

- python3
- Python Image Library (PIL)


Install the dependancies using:

> pip install -r requirements.txt


### Usage:

To use the example `test_main.py` file:

#### Embedding


> Usage: python3 test_main.py e reference_png_input_image_path secret_input_file_path embedded_png_output_image_path

> Eg:    python test_main.py E mario.png dsts.txt t.png

#### Extraction

> Usage: python test_main.py d reference_png_input_image_path secret_output_file_path embedded_png_input_image_path 

> Eg:    python test_main.py D mario.png op.txt t.png

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
