import numpy as np
import cv2

class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""

        regions = dict()
        region_img = np.zeros(image.shape)

        k = 1
        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                
                #Handling edge cases with negative index. Considering them to be default 0
                if(x == 0):
                    image[x - 1, y] = 0
                if(y == 0):
                    image[x, y - 1] = 0
                if(x == 0 and y == 0):
                    image[x - 1, y - 1] = 0

                #          0
                #Case 1: 0 1
                if(image[x, y] == 255 and image[x, y - 1] == 0 and image[x - 1, y] == 0):
                    region_img[x, y] = k
                    k += 1

                #          0
                #Case 2: 1 1
                elif(image[x, y] == 255 and image[x, y - 1] == 0 and image[x - 1, y] == 255):
                    region_img[x, y] = region_img[x - 1, y]

                #          0
                #Case 3: 0 1
                elif(image[x, y] == 255 and image[x, y - 1] == 255 and image[x - 1, y] == 0):
                    region_img[x, y] = region_img[x, y - 1]

                #          1
                #Case 4: 1 1
                elif(image[x, y] == 255 and image[x, y - 1] == 255 and image[x - 1, y] == 255):
                    if(region_img[x, y - 1] == region_img[x - 1, y]):
                        region_img[x, y] = region_img[x, y -1]

                    else:
                        old = region_img[x, y - 1]
                        new = region_img[x - 1, y]
                        region_img[x, y] = new
                        for a in range(0, region_img.shape[0]):
                            for b in range(0, region_img.shape[1]):
                                if(region_img[a, b] == old):
                                    region_img[a, b] = new

        #Adding to dictionaries in term of {region : [pixel1, pixel2]}
        for i in range(1, k + 1):
            for x in range(0, region_img.shape[0]):
                for y in range(0, region_img.shape[1]):
                    if(region_img[x, y] == i):
                        if(i in regions.keys()):
                            regions[i].append((x, y))
                        else:
                            regions.update( {i : [(x, y)]})   
        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)
        statistics = []
        image = np.zeros((254, 256))
        for key in region:
            area = len(region[key])
            
            x = 0
            y = 0

            sum_x = 0
            sum_y = 0
            if (area >= 15):
                for pixel in region[key]:
                    sum_x += pixel[0]
                    sum_y += pixel[1]
                
                #Centroid coordinates
                x = int(sum_x/area)
                y = int(sum_y/area)

                statistics.append((key, area, (y, x))) #Region key, area, centroid (swapped x, y)
                print("Region: %a, Area: %s, Centroid: (%g,%d)" %(key, area, x, y))

        return statistics

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        result_img = image.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        for pair in stats:
            result_img = cv2.putText(result_img, str(pair[0]) + ", " + str(pair[1]), pair[2], font, 0.25, 125)
        return result_img

