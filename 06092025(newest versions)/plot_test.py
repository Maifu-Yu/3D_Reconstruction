import numpy as np
from brainrender import Scene
from brainrender.actors import Points

# --- 参数 ---
annotation_shape = (528, 320, 456)   # atlas 尺寸
threshold        = 30                # 强度阈值
downsample_rate  = 10                 # 降采率：每 5 个取 1 个
max_gap          = 50                 # 最大补洞高度（单位：体素数），Δz<=3 时才补

# --- 加载并阈值提取 coords (假设 coords 存的是 [y, z, x]) ---
data      = np.load("/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/DMPAG_FAM/Coordinate.npy")
intensity = data[...,0]
coords    = np.argwhere(intensity > threshold)  # shape (N,3) 每行 [y,z,x]

coords_mirror = coords.copy()
coords_mirror[:,2] = 456 - coords[:,2]  # x 对称

coords = np.vstack([coords, coords_mirror])

# --- 构建一个空 mask ---
mask_filled = np.zeros(annotation_shape, dtype=bool)

# --- 分组补小洞 ---
# 找到所有独特的 (x,y)
unique_xy, inverse = np.unique(coords[:,1:3], axis=0, return_inverse=True)

for grp_idx, (x, y) in enumerate(unique_xy):
    # 这一组所有的 z
    zs = np.sort(coords[inverse == grp_idx, 0])
    
    # 把原始点先保留
    mask_filled[zs, x, y] = True
    
    # 检查相邻 z 之间的 gap
    for z0, z1 in zip(zs[:-1], zs[1:]):
        gap = z1 - z0
        # 只对小 gap 进行补齐
        if 1 < gap <= max_gap:
            # 把 (z0+1) ... (z1-1) 都标 True
            mask_filled[z0+1 : z1, x, y] = True

# --- 提取补齐后且降采样的点 ---
filled_coords = np.argwhere(mask_filled)          # (M,3)
coords_ds      = filled_coords[::downsample_rate] # 每 5 个取 1 个

# --- 转成实际坐标 (以 25μm 为单位) ---
coords_mm = coords_ds * 25  # [z(mm), x(mm), y(mm)]

# --- 渲染 ---
scene = Scene(atlas_name="allen_mouse_100um", title="")

points_actor = Points(coords_mm, colors="red",alpha=0.2, radius=20)
scene.add_brain_region("PAG", alpha=0.3, color="yellow", silhouette=True)

scene.add(points_actor)



# vlPAG.py
import os
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
from pathlib import Path


# Step 1: 加载注释体
output_dir = '/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/test'
reference_space_key = os.path.join('annotation', 'ccf_2017')
resolution = 25
mcc = MouseConnectivityCache(resolution, reference_space_key, manifest_file=Path(output_dir) / 'manifest.json')
annotation, _ = mcc.get_annotation_volume()
structure_tree = mcc.get_structure_tree(structure_graph_id=1)



# Step 2: 获取 PAG 的结构 ID
pag_id = structure_tree.get_structures_by_name(['Periaqueductal gray'])[0]['id']

# Step 3: 生成 PAG 掩码（3D 布尔矩阵）
mask = annotation == pag_id

# Step 4: 粗略裁剪 vlPAG 区域（caudal + ventral + lateral）
# Allen 25μm Atlas 维度大致为 z=528, y=320, x=456
#mask[:250, :, :] = 0        # rostral
#mask[480:, :, :] = 0        # caudal尾部
#mask[:, :200, :] = 0        # dorsal
#mask[:, :, :300] = 0        # right

mask[:, :115, :] = 0
mask[:, :, 220:236] = 0
mask[:, 200:, :] = 0
mask[:350, :, :] = 0

# Step 5: 提取非零体素坐标（z, y, x）
coords_voxels = np.argwhere(mask)

# Step 6: 体素坐标转换为真实空间坐标（25μm 分辨率 → µm）
# 并按 Brainrender 使用的坐标顺序：[ML, DV, AP] ← [x, y, z]
coords_um = coords_voxels[:, [0, 1, 2]] * 25  # shape: (N, 3), 单位 µm

# Step 7: 创建 Brainrender 场景并添加点云
# 使用 Points actor 渲染点
points_actor2 = Points(coords_um, radius=15, alpha=0.1, colors="#215A7BB1")
scene.add(points_actor2)

#scene.render()






# video
import numpy as np
from brainrender import Scene
from brainrender.actors import Points
from brainrender.video import VideoMaker
import brainrender

# 开启离屏渲染（视频生成时不要打开 GUI 窗口）
brainrender.settings.OFFSCREEN = True

# 创建视频
scene.plotter.camera.Zoom(2)  # 放大视角
vm = VideoMaker(scene, ".", "DMPAG_FAM")
vm.make_video(azimuth=2, duration=12, fps=15)

