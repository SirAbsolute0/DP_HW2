from bz2 import compress
import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        compression = []
        counter = 1
        for x in range(0, binary_image.shape[0]):
            for y in range(0, binary_image.shape[1]):
                if (x == 0 and y == 0):
                    #run length code start with either 0 or 255 (1)
                    if (binary_image[x, y] == 0):
                        compression.append(0)
                    elif (binary_image[x, y] == 255):
                        compression.append(1)

                #Count the following pixels until reach a different value then switch
                elif (binary_image[x, y] == 0 and binary_image[x, y - 1] == 0):
                    counter +=1
                elif (binary_image[x, y] == 0 and binary_image[x, y - 1] == 255):
                    compression.append(counter)
                    counter = 1
                elif (binary_image[x, y] == 255 and binary_image[x, y - 1] == 0):
                    compression.append(counter)
                    counter = 1
                elif (binary_image [x, y] == 255 and binary_image[x, y - 1] == 255):
                    counter += 1
    
        return compression  # replace zeros with rle_code

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        #Create result picture based on height(x) and width(y)
        result = np.zeros((height, width))

        #Get the starting value of rle_code and delete it from the rle_code
        start = rle_code[0]
        rle_code.pop(0)
        
        #Since the first value will be added seperately, -1 on the first counter of the value
        rle_code[0] -= 1
        counter = 0
        last = start

        for x in range(0, result.shape[0]):
            for y in range(0, result.shape[1]):
                #Fist value in the image
                if (x == 0 and y == 0 and start == 0):
                    result[x, y] = 0
                elif (x == 0 and y == 0 and start == 1):
                    result[x, y] = 255

                elif(counter < rle_code[0]):
                    if (last == 0):
                        result[x, y] = 0
                        counter += 1
                    elif (last == 1):
                        result[x, y] = 255
                        counter += 1
                else:
                    if (last == 0):
                        result[x, y] = 255
                        last = 1
                    else:
                        result[x, y] = 0
                        last = 0
                    counter = 1
                    rle_code.pop(0)
                    if(len(rle_code) == 0):
                        return result
            
        return  result  # replace zeros with image reconstructed from rle_Code





        




