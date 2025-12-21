# %%
from solx.components.keyboard.keycap_top import create_keycap_top
from solx.components.keyboard.stem_chocv2 import create_chocv2_stem

top_offset_h = 1.5
add_wd = 2
keycap_top = create_keycap_top(
    bottom_w = 15.0+add_wd,
    bottom_d = 15.0+add_wd,
    top_w = 15.0+add_wd,
    top_d = 15.0+add_wd,
    height = 5.0,
    bottom_radius = 3,
    top_radius = 3,
    top_dx = 0.0,
    top_dy = 0.0,
    top_rx_deg = 5.0,
    top_ry_deg = 0.0,
    top_rz_deg = 0.0,
    dimple = 0.1,
    segments = 64,
    offset_wd = 1,
    offset_h_ratio = 0.5)

keycap_top = keycap_top.translate((0, 0, top_offset_h))
stem = create_chocv2_stem(inverted=False)
keycap = keycap_top + stem

keycap = keycap.rotate_x(180)
keycap.render()
dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
keycap.save_stl(f"{dst_dir_path}/keycap_chocv2_{add_wd}.stl")
# %%
