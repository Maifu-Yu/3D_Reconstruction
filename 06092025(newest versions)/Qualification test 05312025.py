from pathlib import Path
import os
from allensdk.core.reference_space_cache import ReferenceSpaceCache

import numpy as np
import csv
# from collections import Counter


# load the tree
output_dir = '/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output'
reference_space_key = os.path.join('annotation', 'ccf_2017')
resolution = 25
rspc = ReferenceSpaceCache(resolution, reference_space_key, manifest=Path(output_dir) / 'manifest.json')
# ID 1 is the adult mouse structure graph
tree = rspc.get_structure_tree(structure_graph_id=1) 


# load our coordinate data
input_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/Coordinate.npy"
coordinate = np.load(input_file_path)
mask = coordinate[..., 0] > 50
indices = np.array(np.nonzero(mask)).T  # (N, 3), 包含 x, y, z
data = []
values = []
region_ids = []
for x, y, z in indices:
    value = coordinate[x, y, z, 0]
    region_id = coordinate[x, y, z, 1]
    data.append([value, x, y, z, region_id])
    values.append([x,y,z,value])
    region_ids.append([x,y,z,region_id])


# --------
import numpy as np
import nrrd
from allensdk.core.reference_space_cache import ReferenceSpaceCache
from pathlib import Path
import os

class RegionVoxelCounter:
    def __init__(self, annotation_file_path):
        """
        初始化：读取 annotation_25.nrrd 并加载结构树
        """
        # 加载 nrrd 注释体积
        self.annotation_volume, _ = nrrd.read(annotation_file_path)
        self.annotation_volume = np.array(self.annotation_volume)

        # 加载 Allen Brain Atlas 结构树
        self.structure_tree = tree


    def count_voxels(self, region_name, include_descendants=True):
        """
        统计指定区域的体素数量

        参数:
            region_name (str): Allen Brain Atlas 中的区域名称（区分大小写）
            include_descendants (bool): 是否包含所有子区域

        返回:
            int: 体素数量
        """
        # 获取结构信息
        structures = self.structure_tree.get_structures_by_name([region_name])
        if not structures:
            raise ValueError(f"找不到名为 '{region_name}' 的区域")

        region_id = structures[0]['id']

        # 获取区域 ID 列表
        if include_descendants:
            region_ids = self.structure_tree.descendant_ids([region_id])
        else:
            region_ids = [region_id]

        # 统计体素数量
        voxel_mask = np.isin(self.annotation_volume, region_ids)
        voxel_count = np.sum(voxel_mask)
        return voxel_count
'''
def count_volume_mm3(self, region_name, include_descendants=True):
        """
        统计指定区域的体积（单位：mm³）

        返回:
            float: 体积（mm³）
        """
        voxel_count = self.count_voxels(region_name, include_descendants)
        voxel_volume_mm3 = (25e-3) ** 3  # 每个体素体积
        return voxel_count * voxel_volume_mm3
'''
    
annotation_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/CodeFor3D/annotation/annotation_25.nrrd"
counter = RegionVoxelCounter(annotation_path)


def get_levelx_region(level, data):
    level_summary = {}
    unmatched = []
    for val, x, y, z, region_id in data:
        try:
            struct = tree.get_structures_by_id([region_id])[0]
            # 获取最顶层结构（Level 1）
            level_id = struct['structure_id_path'][level]  # [0] 是 root node, [1] 是 Level 1
            level_struct = tree.get_structures_by_id([level_id])[0]            
            #here
            level_name = level_struct['name']
            level_summary.setdefault(level_name, []).append(val)
        except Exception as e:
            # unmatched.append([val, x, y, z, region_id])
            smile = "This line of code in useless, but YOU are not"

    # 保存结果

    output_csv = f"{output_dir}/Output_summary_level_{level}.csv"
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 
                         'Mean_Value', 
                         'Count', 
                         'Voxel_Count', 
                         'Ratio',
                         'MeanValue_times_Count',
                         'PowerDensityWithoutVolume',
                         'PowerDensityWithoutTimes', 
                         'PowerDensity'])
        for name, values in level_summary.items():
            Mean_Value = np.mean(values)
            Count = len(values)
            voxels = int(counter.count_voxels(name))
            Ratio = Count / voxels if voxels > 0 else 0
            MeanValue_times_Count = int(Mean_Value * Count)
            PowerDensityWithoutVolume = (Mean_Value ** 2) * Count
            PowerDensityWithoutTimes = Mean_Value * Count / voxels if voxels > 0 else 0
            PowerDensity = PowerDensityWithoutVolume / voxels if voxels > 0 else 0

            writer.writerow([name, 
                             Mean_Value, 
                             Count, 
                             voxels,
                             Ratio,
                             MeanValue_times_Count,
                             PowerDensityWithoutVolume,
                             PowerDensityWithoutTimes,
                             PowerDensity])

    # 保存无法匹配的点
    '''
    if unmatched:
        unmatched_csv = f"{output_dir}/DMPAG_FAM_unmatched_level_{level}.csv"
        with open(unmatched_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Value', 'X', 'Y', 'Z', 'Region ID'])
            writer.writerows(unmatched)
    '''
    

    print("level",level,"处理完成 ✅")

for level in range(1, 10):
    get_levelx_region(level, data)