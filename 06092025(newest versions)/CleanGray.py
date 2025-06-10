# Yin Liu Modified 0425
# Batches Processing
import cv2 
import os
import numpy as np

folder_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/output folder/Cy3"
save_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/output folder/Cy3_gray"
# folder_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/GFP"
# save_path_raw = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/Gray"
# save_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/CleanGray2"
# import count_files_in_folder from nd2topng_V1_040325.py
# 简化了count功能，后续可以写个package调用

def alg_treshold(img, threshold):
    # 转化为numpy数组
    pixel_array = np.array(img)

    # 创建一个与图像大小相同的布尔数组，用于标记不需要的像素点
    mask = pixel_array < threshold

    # 使用布尔数组索引将不需要的像素点筛掉，设置为 0（让它全黑）
    pixel_array[mask] = 0

    return pixel_array

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        filelocation = os.path.join(folder_path, filename)
        print(filelocation)
        img=cv2.imread(filelocation, cv2.IMREAD_GRAYSCALE)

        # 设置阈值
        threshold = 50
        res_img = alg_treshold(img, threshold)
        cv2.imwrite(os.path.join(save_path , filename.rsplit('.', 1)[0]) + "_CleanGray_" + ".png", res_img)

        '''
        # cv2.imwrite(os.path.join(save_path_raw , filename) + "_Gray_" + ".png", img)
        width = img.shape[1] # 图片宽度
        height = img.shape[0] # 图片高度

        print(img)

        for a in range(height-1): #YL comments--- 这里不需要-1， range这个函数的本身就OK,比如range(10)就是0～9 
            for b in range(width-1): #YL comments--- 这里不需要-1
                if img[a,b] <= 80: # 设定阈值,目前来看100是work的
                    img[a,b] = 0
        cv2.imwrite(os.path.join(save_path , filename) + "_CleanGray_" + ".png", img)
        '''
    # else: #YL comments--- 这里不需要判断else，因为没进if内部自然就会遍历下一个
    #     continue

    # 可以计算所有点的，比如最大最小值，中位数，75%分位数，95%分位数啥的。我们可以把比如xx分位数（比如75%分位数）当作阈值。