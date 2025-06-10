from Transformation_and_Coodinate_with_annotation import Oxyz, parameters
import numpy as np

#folder_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/FAM/ACB"
#csv_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/FAM_single/ACB_FAM_singleMyResults.csv"
#anotation_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/CodeFor3D/annotation/annotation_25.nrrd"



folder_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/input images"
csv_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/input csv/MyResults.csv"
anotation_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/CodeFor3D/annotation/annotation_25.nrrd"

'''

folder_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/allen_100um_images3"
csv_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/allen_100um_images/allenMyResults_F.csv"
anotation_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/CodeFor3D/annotation/annotation_25.nrrd"
'''

a = Oxyz(folder_path, csv_file_path, anotation_path)

# output_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/FAM/test/DMPAG_coordinate0526.npy"

output_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/Coordinate.npy"

np.save(output_file_path, a.coordinate)  # 保存数组
print(f"Array saved to {output_file_path}")

# 得写个百分比，完全没进度，

# 2h for 89 images 还可以

# 大约500多x，200多y，1000多z，z可能是因为背景
# x和y的算法是不是应该换一下
# 验证一下计算方法是不是有问题
