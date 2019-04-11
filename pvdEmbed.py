__author__ = "Tony Josi"
__license__ = "MIT"
__email__ = "tonyjosi.mec@gmail.com"
__status__ = "Production"


"""
************************************************

Usage: python3 pvdEmbed.py <i/p File> <Cover Image> 
Ex:    python3 pvdEmbed.py enc test.png 
Embed data Log can be found as: embedlog.log

************************************************
"""

from PIL import Image
import sys, os

# File Objects creation
input = open(sys.argv[1], "r")
im = Image.open(sys.argv[2])
lg = open("embedlog.log", "w")

# Initialisation
pix = im.load()
hi, wi = im.size

completed = 0
retrieved = ""
count = 0
paddbits = "0000000"

binval = input.read(1)
charNum = 1
if len(binval) == 0:
    print("\nEmpty i/p File!")
    sys.exit("Exiting...")
b = ord(binval)
bitstring = bin(b)
bits = bitstring[2:]

capacity = 0
lix = hi // 3
liy = wi // 3

# Classify pixels based on the difference in pixel value to the number of bits to be substituted to LSB
def classify(pvd):
    nbits = 0
    if pvd < 16:
        nbits = 2
    elif 16 < pvd < 32:
        nbits = 3
    else:
        nbits = 4
    return nbits


# Calculate embedding capacity of the given cover image
def calcCapacity():
    global capacity

    # Divide pixels to [3 x 3] matrix
    for i in range(0, lix * 3, 3):
        for j in range(0, liy * 3, 3):

            # Obtain pixel values of ref. pixel
            rref, gref, bref = pix[i + 1, j + 1]

            # For all pixels in the matrix
            for k in range(i, (i + 3)):
                if k >= hi:
                    break
                for l in range(j, (j + 3)):
                    if k == i + 1 and l == j + 1:
                        continue
                    if l >= wi:
                        break

                    # Calculate the difference in pixel values
                    r, g, b = pix[k, l]
                    rdif = r - rref
                    gdif = g - gref
                    bdif = b - bref
                    rdif = abs(rdif)
                    gdif = abs(gdif)
                    bdif = abs(bdif)

                    # Cumulative capacity
                    capacity = (
                        capacity + classify(rdif) + classify(gdif) + classify(bdif)
                    )

    # Return capacity
    return capacity


# Function to embed data to pixel
def embedbits(i, j, pixel, diff, colorpixel):
    global bits, count, bitstring, paddbits, binval, completed, retrieved, input, charNum

    # Initialise
    pad = 0
    nb = diff

    # If the number of bits required is less than the number of bits in the data(char.) to be Embedded
    if nb < len(bits):

        # Initialise
        newbits = bits[:nb]
        bits = bits[nb:]
        val = colorpixel
        data = newbits
        bival = bin(val)
        bival = bival[2:]
        newbival = bival[: (len(bival) - len(data))] + data

        # Write data to log File for extraction
        lg.write("%s %s %s %s %s %s %s" % (i, j, pixel, diff, pad, charNum, "\n"))

        # Return new pixel value after embedding
        return int(newbival, 2)

    # If the number of bits required is greater than the number of bits in the data(char.) to be Embedded
    else:

        # Apply padding
        newbits = bits + paddbits[: (nb - len(bits))]
        pad = nb - len(bits)
        val = colorpixel
        data = newbits
        bival = bin(val)
        bival = bival[2:]
        newbival = bival[: (len(bival) - len(data))] + data
        count += 1

        # Write data to log File for extraction
        lg.write("%s %s %s %s %s %s %s" % (i, j, pixel, diff, pad, charNum, "\n"))

        # Read new char. for embedding
        binval = input.read(1)

        # Check if file containing data to embed reached its end
        if len(binval) == 0:
            print("Embedding Completed")

            # Close input file object
            input.close()

            # Activate complete flag
            completed = 1

            # Return new pixel value after embedding
            return int(newbival, 2)

        # Check if file containing data to embed havent reached its end
        b = ord(binval)
        bitstring = bin(b)
        bits = bitstring[2:]
        retrieved = ""

        # Increment the char count of embedded data
        charNum += 1

        # Return new pixel value after embedding
        return int(newbival, 2)


# Main Function
def main():

    # Initialise counter containing num of bits embedded till embedding ends
    embedded = 0

    # Print total Embedding capacity
    print("Total Embd. Capacity: ", calcCapacity())

    # Divide pixels to [3 x 3] matrix
    for i in range(0, lix * 3, 3):
        for j in range(0, liy * 3, 3):

            # Obtain pixel values of ref. pixel
            rref, gref, bref = pix[i + 1, j + 1]

            # For all pixels in the matrix
            for k in range(i, (i + 3)):
                if k >= hi:
                    break
                for l in range(j, (j + 3)):
                    if k == i + 1 and l == j + 1:
                        continue
                    if l >= wi:
                        break

                    # Calculate pixel value difference
                    r, g, b = pix[k, l]
                    rdif = r - rref
                    gdif = g - gref
                    bdif = b - bref
                    rdif = abs(rdif)
                    gdif = abs(gdif)
                    bdif = abs(bdif)

                    # Till embedding gets completed
                    if completed == 0:
                        newr = embedbits(k, l, "r", classify(rdif), r)
                    if completed == 0:
                        newg = embedbits(k, l, "g", classify(gdif), g)
                    if completed == 0:
                        newb = embedbits(k, l, "b", classify(bdif), b)

                    # Embedding completed
                    if completed == 1:

                        # Assign modified pixel values
                        pix[k, l] = (newr, newg, newb)

                        # Save embedded image
                        im.save("protest.png")

                        # Close log file
                        lg.close()
                        print("Embedded:", embedded, "bits")

                        # Exit program
                        sys.exit("Done..Exiting main prog.")

                    # Calculate the number of bits embedded
                    embedded = (
                        embedded + classify(rdif) + classify(gdif) + classify(bdif)
                    )

                    # Assign modified pixel values
                    pix[k, l] = (newr, newg, newb)
    # Exit if Data size greater than embedding capacity
    sys.exit("Exiting... Data size greater than embedding capacity!!")


if __name__ == "__main__":
    main()

