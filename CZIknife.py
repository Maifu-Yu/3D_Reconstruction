# CZIknife
# @Time    : 2025/5/9
# @Author  : Maifu
# @Author of annotation  : Maifu

# import sys
# sys.path.append('/Users/stepviewmaifu/anaconda3/lib/python3.11/site-packages/aicspylibczi') # 添加路径 （我的电脑环境的历史遗留问题，一般用户这两行注释掉就好）

# 必须全局做归一化

import os
from aicspylibczi import CziFile
import numpy as np
import cv2


# name_channels要check一下
def cziknife(czi_path, output_dir, num_channels=3, name_channels=["FAM", "Cy3", "DAPI"], scale=0.1):  # If num_channels is not 3 or name_channels is wrong, you must figure it out and set it.
    os.makedirs(output_dir, exist_ok=True)

    # 最多支持6个channels，后续可以优化
    global global_min_0, global_max_0, global_min_1, global_max_1, global_min_2, global_max_2, global_min_3, global_max_3, global_min_4, global_max_4, global_min_5, global_max_5
    global_min_0 = 255
    global_max_0 = 0
    global_min_1 = 255
    global_max_1 = 0
    global_min_2 = 255
    global_max_2 = 0
    global_min_3 = 255
    global_max_3 = 0
    global_min_4 = 255
    global_max_4 = 0
    global_min_5 = 255
    global_max_5 = 0
    for filename in os.listdir(czi_path):
        if filename.endswith(".czi"):
            filelocation = os.path.join(czi_path, filename)
            czi = CziFile(filelocation)
            if not czi.is_mosaic():
                raise ValueError("File is not mosaic image. This package only supports mosaic images.")
            for c in range(num_channels):
                img_c = czi.read_mosaic(C=c, scale_factor=0.05)
                img_c = np.squeeze(img_c)
                if c == 0:
                    global_min_0 = min(global_min_0, img_c.min())
                    global_max_0 = max(global_max_0, img_c.max())
                elif c == 1:
                    global_min_1 = min(global_min_1, img_c.min())
                    global_max_1 = max(global_max_1, img_c.max())
                elif c == 2:
                    global_min_2 = min(global_min_2, img_c.min())
                    global_max_2 = max(global_max_2, img_c.max())
                elif c == 3:
                    global_min_3 = min(global_min_3, img_c.min())
                    global_max_3 = max(global_max_3, img_c.max())
                elif c == 4:
                    global_min_4 = min(global_min_4, img_c.min())
                    global_max_4 = max(global_max_4, img_c.max())
                elif c == 5:
                    global_min_5 = min(global_min_5, img_c.min())
                    global_max_5 = max(global_max_5, img_c.max())
            
    
    for filename in os.listdir(czi_path):
        if filename.endswith(".czi"):
            filelocation = os.path.join(czi_path, filename)
            czi = CziFile(filelocation)

            if not czi.is_mosaic():
                raise ValueError("File is not mosaic image. This package only supports mosaic images.") # Error message
        
            test = czi.read_mosaic(C=0,scale_factor=0.1)
            mosaic_gray = np.squeeze(test).astype(np.float32)
            mosaic_gray = cv2.normalize(mosaic_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            mosaic_gray = mosaic_gray.astype(np.uint8)
            # 阈值分割得到二值图
            # 使用Otsu自动阈值方法将背景与切片分离
            ret, thresh = cv2.threshold(mosaic_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # 如果切片区域反而是黑色（大块白色背景），则反转图像
            if np.mean(thresh) > 127:
                thresh = cv2.bitwise_not(thresh)
            # 可选：形态学操作，去除小孔或噪声
            kernel = np.ones((5,5), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            # 查找轮廓并提取切片边界框
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            slice_bboxes = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                # 忽略面积过小的轮廓（噪声）
                if w*h < 700*700:  # 700*700是一个经验值，可能需要根据实际情况调整
                    continue
                slice_bboxes.append((x, y, w, h))
            # 若需预先尝试使用CZI内部场景(ROI)信息，可用 czi.get_all_mosaic_scene_bounding_boxes() 代替手工分割&#8203;:contentReference[oaicite:5]{index=5}。
            # 对边界框排序，便于命名顺序一致（按y再按x）
            slice_bboxes = sorted(slice_bboxes, key=lambda b: (b[1], b[0]))
            if not slice_bboxes:
                raise ValueError("未检测到任何切片区域，请检查图像或阈值参数。")

            # 5. 计算统一大小：以所有切片的最大宽高为目标尺寸
            max_w = max(b[2] for b in slice_bboxes)
            max_h = max(b[3] for b in slice_bboxes)
            target_size = (max_w, max_h)

        
            for idx, (x, y, w, h) in enumerate(slice_bboxes, start=1):
                for c in range(num_channels):
                    # 读取指定通道的全景图
                    img_c = czi.read_mosaic(C=c,scale_factor=scale)
                    '''
                    分辨率降低后速度很快！而且降低后才能准确切割
                    ''' 
                    img_c = np.squeeze(img_c)  # 去掉第一维
                    # 提取该通道切片区域
                    
                    #rate = scale/0.05
                    
                    norm_slice = img_c[y:y+h, x:x+w].astype(np.float32)
                    
                    # 归一化到0-255并转为uint8(自身归一化)
                    norm_slice_single = cv2.normalize(norm_slice, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
                    norm_slice_single = norm_slice_single.astype(np.uint8)
                    
                    # 用全局范围归一化到0-255
                    if c == 0:
                        norm_slice_global = (norm_slice - global_min_0) / (global_max_0 - global_min_0) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)
                    elif c == 1:
                        norm_slice_global = (norm_slice - global_min_1) / (global_max_1 - global_min_1) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)
                    elif c == 2:
                        norm_slice_global = (norm_slice - global_min_2) / (global_max_2 - global_min_2) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)
                    elif c == 3:
                        norm_slice_global = (norm_slice - global_min_3) / (global_max_3 - global_min_3) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)
                    elif c == 4:
                        norm_slice_global = (norm_slice - global_min_4) / (global_max_4 - global_min_4) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)
                    elif c == 5:
                        norm_slice_global = (norm_slice - global_min_5) / (global_max_5 - global_min_5) * 255
                        norm_slice_global = np.clip(norm_slice_global, 0, 255).astype(np.uint8)

                    resized_global = norm_slice_global
                    resized_single = norm_slice_single

                    # 调整为统一大小
                    #if target_size is not None:
                    #    resized_global = cv2.resize(norm_slice_global, target_size, interpolation=cv2.INTER_AREA)
                    #    resized_single = cv2.resize(norm_slice_single, target_size, interpolation=cv2.INTER_AREA)

                    #else:
                    #    resized_global = norm_slice_global
                    #    resized_single = norm_slice_single

                    # 生成文件名并保存
                    savingfilename = f"{filename}_slice_{idx:02d}_ch_{name_channels[c]}.png"
                    output_dir_c = os.path.join(output_dir, name_channels[c])
                    output_dir_single = os.path.join(output_dir, name_channels[c],"single")
                    filepath_global = os.path.join(output_dir_c, savingfilename)
                    filepath_single = os.path.join(output_dir_single, savingfilename)
                    cv2.imwrite(filepath_global, resized_global)
                    cv2.imwrite(filepath_single, resized_single)
                    print(f"Saved: {savingfilename}")
                    # 加一个自动创建文件夹 暂时需要手动创建

# 自身归一化的也需要，要作为DeepSlice的输入
                
'''
# Example usage
czi_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/testczi"
output_dir = '/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/output folder/'
cziknife(czi_path, output_dir)
'''
