# Batches Processing
import cv2 
import os
folder_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/GFP"
save_path_raw = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/Gray"
save_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/CleanGray2"
# import count_files_in_folder from nd2topng_V1_040325.py
# 简化了count功能，后续可以写个package调用


for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        filelocation = os.path.join(folder_path, filename)
        print(filelocation)
        img=cv2.imread(filelocation, cv2.IMREAD_GRAYSCALE)
        # cv2.imwrite(os.path.join(save_path_raw , filename) + "_Gray_" + ".png", img)
        width = img.shape[1] # 图片宽度
        height = img.shape[0] # 图片高度

        print(img)

        for a in range(height-1):
            for b in range(width-1):
                if img[a,b] <= 80: # 设定阈值,目前来看100是work的
                    img[a,b] = 0
        cv2.imwrite(os.path.join(save_path , filename) + "_CleanGray_" + ".png", img)
    else:
        continue

