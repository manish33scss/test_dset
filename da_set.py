# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 13:21:10 2021

@author: Gaurav
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:29:23 2021
@author: Manish
Enter input directory
enter op directories 
this program will crop a section of an image then translate that cropping area 
using random values, and then take another crop.
so, for every image there will be two crops, and a json file that'll tell the 
crop offset. 
"""

import cv2
import os
import numpy as np
import json
import random




#enter target dir for both crops
targetDir = r"D:\Work\Codes\AI guy tf\Assignment 3\crop_1"
targetDir2 = r"D:\Work\Codes\AI guy tf\Assignment 3\crop_2"

var1 = 0
var2 = 0
var3 = 0
var4 = 0
def check_offset(n,m, upper_left):
        #global var1, var2
        if n > 0 :
            var1 =  ("x :" + str(upper_left[0] - n))
            #print("var1", var1)
            yield var1
        elif n<0:
            var2 =("x : " + str( upper_left[0]- n))
            #print("var2", var2)
            yield var2
        if m < 0 :
            var3 = ("y :" + str( upper_left[1] - m))
            #print("var3", var3)
            yield var3
        elif m > 0 :
            var4= ("y: " + str( upper_left[1] - m))
            yield var4
def load_images_from_folder(folder):
    global images, offset
    images = []
    for filename in os.listdir(folder):
        n = random.randint(5,50)
        m = random.randint(5,60)
        img = cv2.imread(os.path.join(folder,filename))
        num_rows, num_cols = img.shape[:2]
        height, width, channels = img.shape
#center 
        upper_left = (width // 4, height // 4)
        bottom_right = (width * 3 // 4, height * 3 // 4)
        
        
        
        
        translation_matrix = np.float32([ [1,0,n], [0,1,m] ])
        img_translation = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows))
        crop_img_org = img[int(upper_left[1]):int(bottom_right[1]), int(upper_left[0]):int(bottom_right[0])]

        offset = check_offset(n,m,upper_left)
        #print(list(offset))
       
        
        
        crop_img_trans = img_translation[int(upper_left[1]):int(bottom_right[1]), int(upper_left[0]):int(bottom_right[0])]
        #crop_img_trans = img_translation[int(upper_left[1]):int(bottom_right[1]), int(upper_left[0]):int(bottom_right[0])]
        crop_img_org =  cv2.resize(crop_img_org, dsize=(256,256), interpolation=cv2.INTER_CUBIC)
        crop_img_trans =  cv2.resize(crop_img_trans, dsize=(256,256), interpolation=cv2.INTER_CUBIC)

        
        cv2.imwrite(os.path.join(targetDir, filename),crop_img_org)
        cv2.imwrite(os.path.join(targetDir2, filename),crop_img_trans)
        offsetz = list(offset)
        print(offsetz, filename)
        trans_matx = translation_matrix.tolist()
        #rotat_matrix = rotation_matrix.tolist()
        #cv2.imwrite(r'D:\Work\Codes\AI guy tf\Assignment 3\updated\image_{n}.png',img_translation)
        result = {'Filename ' : filename,
                 'offset' : offsetz,
              'Translationmatirx' : json.dumps(trans_matx)}
        
        if img is not None:
            images.append(img)
        file_name = os.path.splitext(filename)[0]
        with open(file_name + ".json", 'w') as outfile:
            json.dump(result, outfile)
    return images

if __name__ == '__main__':
    load_images_from_folder(r"D:\Work\Data\val2017") #input directory