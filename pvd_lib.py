import os
import sys
from PIL import Image

class file_bits_reader:
    
    data = None
    bytes_read_so_far = 0
    total_bytes = 0
    bits_remaining_in_byte_read = 0

    def __init__(self, f_path):
        try:
            self.f_obj = open(f_path, "rb")
            self.data = self.f_obj.read()
            self.total_bytes = len(self.data) 
            self.byte_read = format(self.data[0], '#010b')[2:]
            print(self.data)
            self.bits_read_in_cur_byte = 0
            self.bytes_read_so_far += 1
        except Exception as e:
            if self.f_obj:
                self.f_obj.close()
            print("ERROR: Opening file: {} EXCP: {}".format(f_path, e))

    def get_bits(self, bits):
        if bits > 8 or bits <= 0:
            raise ValueError("Bits should be between 0 and 8 bits")

        eof_status = False
        op_bits = None
        if bits >= (8 - self.bits_read_in_cur_byte) and self.bytes_read_so_far == self.total_bytes:
            eof_status = True
            op_bits = 8 - self.bits_read_in_cur_byte

        read_end = self.bits_read_in_cur_byte + bits
        remaining = 0
        if read_end <= 8:
            remaining = bits
            ret_val = int(self.byte_read[self.bits_read_in_cur_byte:read_end], 2)
            self.bits_read_in_cur_byte += bits
        else:
            remaining = 8 - self.bits_read_in_cur_byte
            ret_val = int(self.byte_read[self.bits_read_in_cur_byte:(self.bits_read_in_cur_byte + remaining)], 2)
            self.bits_read_in_cur_byte += remaining

        if self.bits_read_in_cur_byte == 8 and self.bytes_read_so_far < self.total_bytes:
            self.byte_read = format(self.data[self.bytes_read_so_far], '#010b')[2:]
            self.bytes_read_so_far += 1
            self.bits_read_in_cur_byte = 0

        if self.bits_read_in_cur_byte < 8 and bits - remaining > 0:
            read_end = bits - remaining
            ret_val <<= (bits - remaining)
            ret_val |= int(self.byte_read[self.bits_read_in_cur_byte:(self.bits_read_in_cur_byte+read_end)], 2)
            self.bits_read_in_cur_byte += (bits - remaining)

        if op_bits == None:
            op_bits = bits
        
        return (eof_status, ret_val, op_bits)

    def close_file(self):
        if self.f_obj:
            self.f_obj.close()

class file_bits_writer:
    def __init__(self, f_path):
        try:
            self.f_obj = open(f_path, "wb")
            self.cur_byte = 0
            self.bits_wrote_in_cur_byte = 0
            self.bytes_wrote_to_file_so_far = 0
            self.data = []
        except Exception as e:
            if f_obj:
                f_obj.close()
            print("ERROR: Opening file: {} EXCP: {}".format(f_path, e))

    def set_bits(self, is_eof, bits, data):
        if bits > 8 or bits <= 0:
            raise ValueError("Bits should be between 0 and 8 bits")

        if self.bits_wrote_in_cur_byte + bits <= 8:
            self.cur_byte <<= bits
            self.cur_byte |= data
            self.bits_wrote_in_cur_byte += bits
        else:
            remaining_reqd = 8 - self.bits_wrote_in_cur_byte
            bits_str = bin(data)[2:].zfill(bits)
            if remaining_reqd > 0:  
                self.cur_byte <<= remaining_reqd
                self.cur_byte |= int(bits_str[:remaining_reqd], 2)
                self.bits_wrote_in_cur_byte += remaining_reqd
            self.data.append(self.cur_byte)
            self.cur_byte = 0
            self.bits_wrote_in_cur_byte = 0
            self.bytes_wrote_to_file_so_far += 1
            self.bits_wrote_in_cur_byte += (bits - remaining_reqd)
            self.cur_byte <<= (bits - remaining_reqd)
            self.cur_byte |= int(bits_str[remaining_reqd:], 2) 

        if is_eof:
            self.data.append(self.cur_byte)
            self.bytes_wrote_to_file_so_far += 1
            self.close_file()

    def close_file(self):
        if self.f_obj:
            print(self.data)
            self.f_obj.write(bytes(self.data))
            self.f_obj.close()


class pvd_lib:

    def __init__(self):
        pass

    @staticmethod
    def _pvd_table(p_diff):
        nbits = 0
        if p_diff < 16:
            nbits = 2
        elif 16 < p_diff < 32:
            nbits = 3
        else:
            nbits = 4
        return nbits

    @staticmethod
    def _embed_capacity(ref_image_path):

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

                            embed_capacity += pvd_lib._pvd_table(abs(c_rgb[0] - ref_rgb[0])) + \
                                pvd_lib._pvd_table(abs(c_rgb[1] - ref_rgb[1])) + \
                                    pvd_lib._pvd_table(abs(c_rgb[2] - ref_rgb[2]))
            
        print(embed_capacity // 8)
        return embed_capacity // 8

    @staticmethod
    def replace_lsbs(pixel, bits, value):
        mask = (1 << bits) - 1
        pixel &= (~mask)
        return (pixel | value)

    @staticmethod
    def get_lsbs(pixel, bits):
        mask = (1 << bits) - 1
        pixel &= (mask)
        return (pixel)

    def embed_data(self, ref_image_path):
    
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

                            embed_capacity += pvd_lib._pvd_table(abs(c_rgb[0] - ref_rgb[0])) + \
                                pvd_lib._pvd_table(abs(c_rgb[1] - ref_rgb[1])) + \
                                    pvd_lib._pvd_table(abs(c_rgb[2] - ref_rgb[2]))
            
        return embed_capacity // 8

    def pvd_embed(self, ref_image_path, secret_file_path):
        
        embed_cap = pvd_lib._embed_capacity(ref_image_path)
        s_f_size = os.path.getsize(secret_file_path)

        if embed_cap < s_f_size:
            print("ERROR: Secret file size is more than embedding capacity of image - " \
                "Embedding capacity: {} bytes, Secret file size: {} bytes".format(embed_cap, s_f_size))



""" Test """
if __name__ == "__main__":
    pvd_obj = pvd_lib()
    #pvd_obj._embed_capacity(sys.argv[1])
    pvd_obj.pvd_embed(sys.argv[1], sys.argv[2])