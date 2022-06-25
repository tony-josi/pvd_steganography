import sys

from pvd_lib import pvd_lib

""" Test """
if __name__ == "__main__":

    pvd_obj = pvd_lib()

    if sys.argv[1] == 'e' or sys.argv[1] == 'E':
        pvd_obj.pvd_embed(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] =='d' or sys.argv[1] == 'D':
        pvd_obj.pvd_extract(sys.argv[2], sys.argv[3], sys.argv[4])
