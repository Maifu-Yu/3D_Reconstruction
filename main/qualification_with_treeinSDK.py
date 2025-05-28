from pathlib import Path
import os
from allensdk.core.reference_space_cache import ReferenceSpaceCache

import numpy as np
import csv
from collections import Counter


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
mask = coordinate[..., 0] > 0
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


def get_levelx_region(level, data):
    level_summary = {}
    unmatched = []
    for val, x, y, z, region_id in data:
        try:
            struct = tree.get_structures_by_id([region_id])[0]
            # 获取最顶层结构（Level 1）
            level_id = struct['structure_id_path'][level]  # [0] 是 root node, [1] 是 Level 1
            level_struct = tree.get_structures_by_id([level_id])[0]
            level_name = level_struct['name']
            level_summary.setdefault(level_name, []).append(val)
        except Exception as e:
            # unmatched.append([val, x, y, z, region_id])
            smile = "This line of code in useless, but YOU are not"

    # 保存结果

    output_csv = f"{output_dir}/DMPAG_FAM_summary_level_{level}.csv"
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 'Mean Value', 'Count'])
        for name, values in level_summary.items():
            writer.writerow([name, np.mean(values), len(values)])

    # 保存无法匹配的点
    if unmatched:
        unmatched_csv = f"{output_dir}/DMPAG_FAM_unmatched_level_{level}.csv"
        with open(unmatched_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Value', 'X', 'Y', 'Z', 'Region ID'])
            writer.writerows(unmatched)

    print("level",level,"处理完成 ✅")

for level in range(1, 10):
    get_levelx_region(level, data)