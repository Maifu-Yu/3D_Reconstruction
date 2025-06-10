# Functions
# -*- coding: utf-8 -*-
# @Time    : 2025/4/23
# @Author  : Maifu

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
