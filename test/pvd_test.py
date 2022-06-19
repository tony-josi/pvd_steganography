# class file_bits_reader:
    
#     data = None
#     bytes_read_so_far = 0
#     total_bytes = 0
#     bits_remaining_in_byte_read = 0

#     def __init__(self, f_path):
#         try:
#             #f_obj = open(f_path, "r")
#             self.data = [0xA, 0xDE, 0x1]
#             self.total_bytes = len(self.data) 
#             self.byte_read = format(self.data[0], '#010b')[2:]
#             self.bits_read_in_cur_byte = 0
#             self.bytes_read_so_far += 1
#         except:
#             if f_obj:
#                 f_obj.close()
#             print("ERROR: Opening file: {}".format(f_path))

#     def get_bits(self, bits):
#         if bits > 8 or bits <= 0:
#             raise ValueError("Bits should be between 0 and 8 bits")

#         #print(self.byte_read)

#         eof_status = False
#         if bits >= (8 - self.bits_read_in_cur_byte) and self.bytes_read_so_far == self.total_bytes:
#             eof_status = True

#         read_end = self.bits_read_in_cur_byte + bits
#         remaining = 0
#         if read_end <= 8:
#             remaining = bits
#             ret_val = int(self.byte_read[self.bits_read_in_cur_byte:read_end], 2)
#             self.bits_read_in_cur_byte += bits
#         else:
#             remaining = 8 - self.bits_read_in_cur_byte
#             ret_val = int(self.byte_read[self.bits_read_in_cur_byte:(self.bits_read_in_cur_byte + remaining)], 2)
#             self.bits_read_in_cur_byte += remaining

#         if self.bits_read_in_cur_byte == 8 and self.bytes_read_so_far < self.total_bytes:
#             self.byte_read = format(self.data[self.bytes_read_so_far], '#010b')[2:]
#             self.bytes_read_so_far += 1
#             self.bits_read_in_cur_byte = 0

#         if bits - remaining > 0:
#             read_end = bits - remaining
#             ret_val <<= (bits - remaining)
#             ret_val |= int(self.byte_read[self.bits_read_in_cur_byte:read_end], 2)
#             self.bits_read_in_cur_byte += (bits - remaining)
        
#         return (eof_status, ret_val)

# if __name__ == "__main__":
#     obj = file_bits_reader("f")

#     print("{0:b}".format(obj.data[0]))
#     print("{0:b}".format(obj.data[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(2)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(2)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(3)
#     print(val[0])
#     print("{0:b}".format(val[1]))

#     val = obj.get_bits(2)
#     print(val[0])
#     print("{0:b}".format(val[1]))

import sys
import random

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
            #print("read: {}".format(self.data[0]))
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

        #print(self.byte_read)

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
            #print("read: {}".format(self.data[self.bytes_read_so_far]))
            self.bytes_read_so_far += 1
            self.bits_read_in_cur_byte = 0

        if self.bits_read_in_cur_byte < 8 and bits - remaining > 0:
            read_end = bits - remaining
            ret_val <<= (bits - remaining)
            #print(self.bits_read_in_cur_byte, read_end, remaining)
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
            #print("wrote: {}".format(self.cur_byte))
            #self.f_obj.write(bytes(self.cur_byte))
            self.data.append(self.cur_byte)
            #print("wrote: {}".format(self.cur_byte))
            self.cur_byte = 0
            self.bits_wrote_in_cur_byte = 0
            self.bytes_wrote_to_file_so_far += 1
            self.bits_wrote_in_cur_byte += (bits - remaining_reqd)
            self.cur_byte <<= (bits - remaining_reqd)
            self.cur_byte |= int(bits_str[remaining_reqd:], 2) 

        if is_eof:
            #self.f_obj.write(bytes(self.cur_byte))
            self.data.append(self.cur_byte)
            self.bytes_wrote_to_file_so_far += 1
            self.close_file()

    def close_file(self):
        if self.f_obj:
            print(self.data)
            self.f_obj.write(bytes(self.data))
            self.f_obj.close()



if __name__ == "__main__":

    obj = file_bits_reader(sys.argv[1])
    wobj = file_bits_writer(sys.argv[2])
    possible_bits = [2, 3, 4]
    while True:
        bits = random.choice(possible_bits)
        val = obj.get_bits(bits)
        #print("Bits: {}, Data: {}".format(bits, bin(val[1])))
        wobj.set_bits(val[0], val[2], val[1])
        if val[0] == True:
            break

    print(wobj.bytes_wrote_to_file_so_far)