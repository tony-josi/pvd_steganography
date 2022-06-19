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

            if no_of_matrix_h < 1 or no_of_matrix_w < 0:
                return embed_capacity;

            for width_itr in range(0, no_of_matrix_w * 3, 3):
                for height_itr in range(0, no_of_matrix_h * 3, 3):

                    rref, gref, bref = pixels[width_itr + 1, height_itr + 1]

                    for w_i in range(width_itr, width_itr + 3):
                        for h_j in range(height_itr, height_itr + 3):

                            if w_i == width_itr + 1 or h_j == height_itr + 1:
                                continue

                            c_rref, c_gref, c_bref = pixels[w_i, h_j]

                            embed_capacity += self._pvd_table(abs(c_rref - rref)) + \
                                self._pvd_table(abs(c_gref - gref)) + \
                                    self._pvd_table(abs(c_bref - bref))
            
        #print(embed_capacity // 8)
        return embed_capacity // 8

    def pvd_embed(self, ref_image_path, secret_file_path):
        pass


""" Test """
if __name__ == "__main__":
    pvd_obj = pvd_lib()
    pvd_obj._embed_capacity(sys.argv[1])