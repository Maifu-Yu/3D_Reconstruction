# Batches Processing
# -*- coding: utf-8 -*-
# @Time    : 2025/4/25
# @Author  : Maifu
# @Author of annotation  : Maifu

import cv2 
import os
import numpy as np
import csv
import nrrd

# 需要缩小，研究一下多少的分辨率能让它们不冲突


class parameters():
    def __init__(self, csv_file_path, target_filename=None):
        self.Filename_column = []
        self.ox_column = []
        self.oy_column = []
        self.oz_column = []
        self.ux_column = []
        self.uy_column = []
        self.uz_column = []
        self.vx_column = []
        self.vy_column = []
        self.vz_column = []
        self.DS_result = None
        self.load_csv(csv_file_path)
        self.get_parameters(target_filename) if target_filename else None
        # 初始化参数

    def load_csv(self, csv_file_path):
        with open(csv_file_path, newline='') as file:
            self.DS_result = list(csv.DictReader(file))
            self.Filename_column = [row['Filenames'] for row in self.DS_result]
            self.ox_column = [float(row['ox']) for row in self.DS_result]
            self.oy_column = [float(row['oy']) for row in self.DS_result]
            self.oz_column = [float(row['oz']) for row in self.DS_result]
            self.ux_column = [float(row['ux']) for row in self.DS_result]
            self.uy_column = [float(row['uy']) for row in self.DS_result]
            self.uz_column = [float(row['uz']) for row in self.DS_result]
            self.vx_column = [float(row['vx']) for row in self.DS_result]
            self.vy_column = [float(row['vy']) for row in self.DS_result]
            self.vz_column = [float(row['vz']) for row in self.DS_result]
            # 提取列作为新的列表，方便用索引

    def get_parameters(self, target_filename):
        index = next((i for i, item in enumerate(self.Filename_column) if item == target_filename), None)
        if index is not None:
            global ox, oy, oz, ux, uy, uz, vx, vy, vz
            ox = self.ox_column[index]
            oy = self.oy_column[index]
            oz = self.oz_column[index]
            ux = self.ux_column[index]
            uy = self.uy_column[index]
            uz = self.uz_column[index]
            vx = self.vx_column[index]
            vy = self.vy_column[index]
            vz = self.vz_column[index]
            return ox, oy, oz, ux, uy, uz, vx, vy, vz, index
        else:
            return None

# Example usage
# a=parameters('/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/GFPMyResults.csv',"DMH-1419-12-2_0001.nd2_channel_FITC_s089.png")
# print(a)
# print(a.ox_column)    
# print(a.ox_column[10])
# print(ox)


# Rotation
class Oxyz:
    def __init__(self, folder_path, csv_file_path, anotation_path): # folder_path是图片文件夹的路径，csv_file_path是csv文件的路径
        self.folder_path = folder_path
        self.coordinate = np.zeros((600, 600, 600, 2)) # WHS Rat 39 um  x=511, y=1023, Z=511  ABA Mouse 25 um  X=455, y=527, z=319       ANO.shape=(528, 320, 456), 所以应该也是y, z, x的顺序
        # 我懂了！QUICKNII的y本身就是AP（最长），而deepslice用的就是那一套， z是DV，x是ML，所以应该是y, z, x的顺序
        
        # self.coordinate_result = np.zeros((550, 550, 550, 2))
        self.search = parameters(csv_file_path)
        self.width = 0
        self.height = 0
        self.Rotation(anotation_path)

    def readANO(self, anotation_path):
        self.ANO, self.metaANO = nrrd.read(anotation_path)
        ANO = np.array(self.ANO)
        self.ANO = ANO
        return ANO

    def RotationCalculation(self, x_2D, y_2D):
        global x, y, z
        # 计算新的坐标系

        x = int((ox + (ux * x_2D)/self.width + (vx * y_2D)/self.height))
        y = int((oy + (uy * x_2D)/self.width + (vy * y_2D)/self.height)) 
        z = int((oz + (uz * x_2D)/self.width + (vz * y_2D)/self.height))

        # 应该提供选项, 选择alignment的nrrd文件，并改变缩放倍数
        return x, y, z

    def Rotation(self,anotation_path):
        self.readANO(anotation_path)
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                filelocation = os.path.join(self.folder_path, filename)
                self.search.get_parameters(filename)  # get the parameters from the csv file, (ox,oy,oz,ux,uy,uz,vx,vy,vz as global variables)
                self.img=cv2.imread(filelocation, cv2.IMREAD_GRAYSCALE) # read the image
                self.width = self.img.shape[1]
                self.height = self.img.shape[0]
                print(filelocation)
                for y_2D in range(self.height):
                    for x_2D in range(self.width):  # 降噪也可以加在这里
                        pixel_value = self.img[y_2D, x_2D]
                        if 0 < pixel_value: # 降噪，暂时关闭了，这里应该设置一个布尔值供用户选择是否降噪的 # 200是因为allen brain的背景基本都很高，实际使用时不需要200，或者供用户选择
                            # print(x_2D, y_2D)
                            self.RotationCalculation(self.width - x_2D, self.height - y_2D)
                            self.coordinate[(527-y),(z),(x), 0] = self.img[y_2D, x_2D] # save the new coordinate
                            # 坐标换算成Allen CCFv3的坐标体系
                            # self.coordinate_result[x, y, z, 0] = self.coordinate[(527-y),(319-z),x, 0]
                            #try:
                            #    self.coordinate[(527-y),(319-z),x, 1] = self.ANO[(527-y),(319-z),x]  # Mingyang好像是z,y,x.这里需要查证一下  https://www.nitrc.org/plugins/mwiki/index.php?title=quicknii:Coordinate_systems
                            #except:
                            #    self.coordinate[(527-y),(319-z),x, 1] = 0
                            try:
                                self.coordinate[(527-y),(z),x, 1] = self.ANO[(527-y),(z),x]  # Mingyang好像是z,y,x.这里需要查证一下  https://www.nitrc.org/plugins/mwiki/index.php?title=quicknii:Coordinate_systems
                            except:
                                self.coordinate[(527-y),(z),x, 1] = 0

                            # 理论上应该是[AP, DV, ML]，但是somehow我的坐标系里[y, z, x]才work，应该对应DV, AP, ML



# first_channel = coordinate[..., 0]  # shape: (200, 200, 200)
# second_channel = coordinate[..., 1] # shape: (200, 200, 200)


# self.parameters = parameters(csv_file_path)
        


# rotation和建立新的坐标系1是同一步，然后每隔一段距离取平面
# 用annotation再建立一个新的坐标系2
# Registion完成，进行qualification

# Oxy("/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/GFP/DMH-1419-12-2_0001.nd2_channel_FITC_s089.png")




'''

# Example usage
folder_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/RotationTest"
csv_file_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/GFPMyResults.csv"
a = Oxyz(folder_path, csv_file_path)

print(a.coordinate)

print(a.coordinate.max())


output_file_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/RotationTest/output.txt"

# a.coordinate = a.coordinate.astype(np.uint8)  # 转换为uint8类型

output_file_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/RotationTest/coordinate.npy"
np.save(output_file_path, a.coordinate)  # 保存数组
print(f"Array saved to {output_file_path}")

# 加载数组
# loaded_array = np.load(output_file_path)
# print("Loaded array:")
# print(loaded_array)
# print("Shape:", loaded_array.shape)

'''
# 问题
# 原图像素太高了，由于赋值是迭代，可能出现问题，好几个像素点赋值给同一个坐标了，需要使用刘老师的脚本，也许最好缩到和标准的Allen brain一样的尺寸。而且，非常慢，3张图片跑了十几分钟
# 另外，如果坐标值是整数，可能会出现问题，应该要设置为浮点数，这一步还没有做，坐标能不能是浮点数？？?
'''
'''

# 如果能即时显示3D图就好了

# 加个进度条和计时的，记录第一个图片的时间，然后乘以图片数
