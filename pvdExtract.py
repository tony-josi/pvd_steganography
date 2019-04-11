__author__ = "Tony Josi"
__license__ = "MIT"
__email__ = "tonyjosi.mec@gmail.com"
__status__ = "Production"


"""
************************************************

Usage: python3 pvdExtract.py <Embedded Cover Image File> <Output File> 
Ex:    python3 pvdExtract.py protest.png cipher

************************************************
"""

from PIL import Image
import sys, os

# File Objects creation
im = Image.open(sys.argv[1])
outp = open(sys.argv[2], "w")
lg = open("embedlog.log", "r")

# Initialisation
pix = im.load()
temp = 1
chrtr = ""

# Main Function
def main():
    global chrtr, temp
    while True:

        # Read each line from log file
        st = lg.readline()

        # Check if log file reached its end
        if len(st) == 0:
            # Write extracted data to file
            # print(chr(int(chrtr, 2)))
            outp.write(chr(int(chrtr, 2)))
            break

        # Unpack line read from log file to variables
        i, j, pixel, diff, pad, charNum = st.split()

        # Process variables
        i = int(i)
        j = int(j)
        diff = int(diff)
        pad = int(pad)
        charNum = int(charNum)
        r, g, b = pix[i, j]

        # Check if a new character in embed log is reached
        if temp != charNum:
            # print(chr(int(chrtr, 2)), end="")
            outp.write(chr(int(chrtr, 2)))
            chrtr = ""

        # If embedded pixel is red
        if pixel == "r":
            binr = bin(r)
            chrtr += binr[(len(binr) - diff) :]

        # If embedded pixel is green
        if pixel == "g":
            binr = bin(g)
            chrtr += binr[(len(binr) - diff) :]

        # If embedded pixel is blue
        if pixel == "b":
            binr = bin(b)
            chrtr += binr[(len(binr) - diff) :]

        # Unpad if padding is done
        if pad != 0:
            chrtr = chrtr[: (len(chrtr) - pad)]

        # For checking if character has changed in embed file
        temp = charNum

    # Close file objects
    outp.close()
    lg.close()
    print("Extracting to the file:", sys.argv[2])
    print("Extraction completed...  Exiting!")


if __name__ == "__main__":
    main()
