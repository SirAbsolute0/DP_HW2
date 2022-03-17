import math
from unittest import skip

class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0]*256

        #Each value in the image will be map to an array element
        for x in range(0, image.shape[0]):
            for y in range (0, image.shape[1]):
                hist[image[x, y]] += 1

        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""

        with_class_var = 0
        lowest = math.inf
        result = 0

        for threashold in range(0, len(hist)):
            weight_b = 0
            mean_b = 0
            variance_b = 0

            weight_f = 0
            mean_f = 0
            variance_f = 0

            sum_b = sum(hist[0 : threashold])
            sum_f = sum(hist[threashold : 255])

            #Calculating background information
            if ( sum_b == 0):
                weight_b = 0
                mean_b = 0
                variance_b = 0
            else:
                weight_b = sum_b/sum(hist)
                
                for value in range(0, threashold):
                    mean_b += (value * hist[value])/sum_b

                for value in range(0, threashold):
                    variance_b += ((value - mean_b)**2 * hist[value])/sum_b
            
            #Calculating forground information
            if (sum_f == 0):
                weight_f = 0
                mean_f = 0
                variance_f = 0
            else:
                weight_f = sum(hist[threashold : len(hist)])/sum(hist)
                
                for value in range(threashold, len(hist)):
                    mean_f += (value * hist[value])/sum_f

                for value in range(threashold, len(hist)):
                    variance_f += ((value - mean_f)**2 * hist[value])/sum_f

            #Finding the optimal threashold based on the lowest within class variance
            with_class_var = weight_b*(variance_b) + weight_f*(variance_f)
            if(with_class_var < lowest):
                lowest = with_class_var
                result = threashold
          
        return result

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""
        
        bin_img = image.copy()

        hist = BinaryImage.compute_histogram(self, image)
        threshold = BinaryImage.find_otsu_threshold(self, hist)

        #Binarized image based on Otsu's threashold
        for x in range(0, bin_img.shape[0]):
            for y in range (0, bin_img.shape[1]):
                if (bin_img[x, y] < threshold):
                    bin_img[x, y] = 255
                    
                elif (bin_img[x, y] >= threshold):
                    bin_img[x, y] = 0
        return bin_img


