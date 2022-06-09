import os
import sys
from PIL import Image

class pvd_lib:

    def __init__(self):
        pass

    def _pvd_table(self, p_diff):
        nbits = 0
        if p_diff < 16:
            nbits = 2
        elif 16 < p_diff < 32:
            nbits = 3
        else:
            nbits = 4
        return nbits

    def _embed_capacity(self, ref_image_path):

        embed_capacity = 0
        
        with Image.open(ref_image_path) as img_obj:
            pixels = img_obj.load()
            img_height, img_width = img_obj.size
            #print(img_height, img_width)
            
            no_of_matrix_h = img_height // 3 - 1
            no_of_matrix_w = img_width // 3 - 1

            if no_of_matrix_h < 1 or no_of_matrix_w < 1 or len(pixels[0, 0]) < 3:
                return embed_capacity;

            for height_itr in range(0, no_of_matrix_h * 3, 3):
                for width_itr in range(0, no_of_matrix_w * 3, 3):

                    #print(pixels[width_itr + 1, height_itr + 1])
                    ref_rgb = pixels[height_itr + 1, width_itr + 1]

                    for h_j in range(height_itr, height_itr + 3):
                        for w_i in range(width_itr, width_itr + 3):

                            if w_i == width_itr + 1 or h_j == height_itr + 1:
                                continue

                            c_rgb = pixels[h_j, w_i]

                            embed_capacity += self._pvd_table(abs(c_rgb[0] - ref_rgb[0])) + \
                                self._pvd_table(abs(c_rgb[1] - ref_rgb[1])) + \
                                    self._pvd_table(abs(c_rgb[2] - ref_rgb[2]))
            
        print(embed_capacity // 8)
        return embed_capacity // 8

    def pvd_embed(self, ref_image_path, secret_file_path):
        
        embed_cap = self._embed_capacity(ref_image_path)
        s_f_size = os.path.getsize(secret_file_path)

        if embed_cap < s_f_size:
            print("ERROR: Secret file size is more than embedding capacity of image - " \
                "Embedding capacity: {} bytes, Secret file size: {} bytes".format(embed_cap, s_f_size))



""" Test """
if __name__ == "__main__":
    pvd_obj = pvd_lib()
    #pvd_obj._embed_capacity(sys.argv[1])
    pvd_obj.pvd_embed(sys.argv[1], sys.argv[2])