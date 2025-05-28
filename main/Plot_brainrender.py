from brainrender import Scene
from brainrender.actors import Points
import numpy as np

data = np.load("/Users/stepviewmaifu/RESEARCH/Fu lab/3D working folder/output/Coordinate.npy")
# data = np.transpose(coordinate, (2, 1, 0, 3))
# data = np.load("/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/allen_100um_images_front_coordinate.npy")

# Split intensity and region ID channels
intensity = data[..., 0]
region_id  = data[..., 1]

del data  # Free up memory

# Filter for voxels with intensity > 0
mask = intensity > 0
coords = np.argwhere(mask)        # indices of nonzero-intensity voxels (as (x, y, z))
# region_ids = region_id[mask]      # corresponding region IDs

del intensity, region_id, mask  # Free up memory

# Convert voxel indices to millimeters (100 μm = 0.1 mm)
# If needed, reorder axes to [z, y, x] for Brainrender (AP, DV, ML):
# coords_µm = coords[:, [2, 1, 0]] * 0.1  # (N×3 array of [AP, DV, ML] in mm)


# z,x,y 由于 已经变换过一个y,z,x，所以是x,y,z 所以对于brainrender不需要做变化？用QuckNII的坐标系就可以（并乘缩放倍数）？需要思考一下，，，
# 断层的方向看着还是不对，可能还是需要做变化

# coords = coords[:, [0, 2, 1]] * 25 # make sense 只有这一种搭配方式是对称的
coords = coords[:, [0, 1, 2]] * 25  


# (Optional) Color points by region ID, using a simple colormap
'''
try:
    import matplotlib.pyplot as plt
    unique = np.unique(region_ids)
    cmap = plt.cm.viridis(np.linspace(0, 1, len(unique)))
    id_to_color = {uid: cmap[i] for i, uid in enumerate(unique)}
#    point_colors = [id_to_color[rid] for rid in region_ids]
    point_colors = [id_to_color[rid][:3] for rid in region_ids]
except ImportError:
    # If matplotlib not available, use a default color (e.g. red)
    point_colors = "red"
'''

# Create a Points actor and add to a Brainrender scene
points_actor = Points(coords, colors="red", radius=25)
scene = Scene(atlas_name="allen_mouse_25um", title="Intensity > 0 voxels")
scene.add(points_actor)
scene.render()


'''
# 创建场景
scene = Scene(atlas_name="allen_mouse_100um")

# 读取你的点（单位：μm），然后换算为 mm（brainrender 用 mm）
coordinate = np.load("/Users/stepviewmaifu/🚀RESEARCH🚀/Fu lab/3D test data/output folder 5:15:2025/Cy3_coordinate.npy")
coordinate = np.transpose(coordinate, (2, 1, 0, 3))
mask = coordinate[..., 0] > 0
indices = np.array(np.nonzero(mask)).T  # shape: (N, 3)
points_mm = indices * 1  # Allen 25um 分辨率换算成 mm
    
# 创建 Points actor
points_actor = Points(points_mm, colors="crimson", radius=50)

# 添加到 scene 中
scene.add(points_actor)

# 渲染
scene.render()
'''
