# Batches Processing
# -*- coding: utf-8 -*-
# @Time    : 2025/4/25
# @Author  : Maifu
# @Author of annotation  : Maifu

import cv2 
import os
import numpy as np
import csv



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
    def __init__(self, folder_path, csv_file_path): # folder_path是图片文件夹的路径，csv_file_path是csv文件的路径
        self.folder_path = folder_path
        self.coordinate = np.zeros((2000, 2000, 2000))
        self.search = parameters(csv_file_path)
        self.width = 0
        self.height = 0
        self.Rotation()

    def RotationCalculation(self, x_2D, y_2D):
        global x, y, z
        # 计算新的坐标系
        x = int(ox + (ux * x_2D)/self.width + (vx * y_2D)/self.height)
        y = int(oy + (uy * x_2D)/self.width + (vy * y_2D)/self.height)
        z = int(oz + (uz * x_2D)/self.width + (vz * y_2D)/self.height)
        return x, y, z

    def Rotation(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".png"):
                filelocation = os.path.join(self.folder_path, filename)
                self.search.get_parameters(filename)  # get the parameters from the csv file, (ox,oy,oz,ux,uy,uz,vx,vy,vz as global variables)
                self.img=cv2.imread(filelocation, cv2.IMREAD_GRAYSCALE) # read the image
                self.width = self.img.shape[1]
                self.height = self.img.shape[0]
                print(filelocation)
                for x_2D in range(self.height):
                    for y_2D in range(self.width):  # 降噪也可以加在这里
                        if self.img[x_2D, y_2D] > 100:
                            print(x_2D, y_2D)
                            self.RotationCalculation(x_2D, y_2D)
                            self.coordinate[x, y, z] = self.img[x_2D, y_2D] # save the new coordinate
                
        


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

# 原图像素太高了，由于赋值是迭代，可能出现问题，好几个像素点赋值给同一个坐标了，需要使用刘老师的脚本，也许最好缩到和标准的Allen brain一样的尺寸。而且，非常慢，3张图片跑了十几分钟

output_file_path = "/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/RotationTest/output.txt"

with open(output_file_path, "w") as file:
    file.write(str(a.coordinate))  # 将 a.coordinate 转换为字符串并写入文件 # 后续改进：如json文件，将metadata写在前面

print(f"Data saved to {output_file_path}")
'''