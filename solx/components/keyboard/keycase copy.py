# %%
from solid import linear_extrude, polygon

from solx import Cube, SolxObject

#####################################
##### case point layout
#  ↑y
# →x
# pt0-------------------pt1
#  |                     |
#  |   pt5-----pt4       |
# pt7--pt6     pt3------pt2
#
### bottom case z axis layout
# xx btm_z2
# xxx btm_z1
# xxxxxx btm_z0
######################################

# R
points = [(189.0, 55.0), (77.0, 55.0), (77.0, 150.0), (118.0, 150.0), (118.0, 121.0), (158.895, 121.0), (158.895, 150.0), (189.0, 150.0)]



points = [(x, -y) for x, y in points]


pt1 = points[0]
pt0 = points[1]
pt7 = points[2]
pt6 = points[3]
pt5 = points[4]
pt4 = points[5]
pt3 = points[6]
pt2 = points[7]

def shift_points(mgn):
    dst_points = [
        (pt0[0] - mgn, pt0[1] + mgn),
        (pt1[0] + mgn, pt1[1] + mgn),
        (pt2[0] + mgn, pt2[1] - mgn),
        (pt3[0] - mgn, pt3[1] - mgn),
        (pt4[0] - mgn, pt4[1] - mgn),
        (pt5[0] + mgn, pt5[1] - mgn),
        (pt6[0] + mgn, pt6[1] - mgn),
        (pt7[0] - mgn, pt7[1] - mgn),
    ]
    return dst_points

inner_mgn = 0.15
outer_mgn = 1.0
outer_points = shift_points(outer_mgn)
inner_points = shift_points(inner_mgn)
bottom_height = 1.0
total_height = 5.0
base_height = total_height - bottom_height
base_plate = SolxObject(linear_extrude(height=base_height)(
    polygon(points=inner_points)
))
outer_height = total_height
outer_plate = SolxObject(linear_extrude(height=outer_height)(
    polygon(points=outer_points)
))

# %%


# %%
base_plate.render()
# %%
box = outer_plate - base_plate.translate((0, 0, bottom_height))
box.render()
# %%
def create_sub_part(
    pos1,
    pos2,
    directon,
    height,
    direction_length) -> SolxObject:
    p1 = pos1
    p2 = (pos1[0] + directon[0] * direction_length, pos1[1] + directon[1] * direction_length)
    p3 = (pos2[0] + directon[0] * direction_length, pos2[1] + directon[1] * direction_length)
    p4 = pos2
    sub_part = SolxObject(linear_extrude(height=height)(
        polygon(points=[p1, p2, p3, p4])
    ))
    return sub_part
# マウス周りは外を除去
ip = inner_points
box -= create_sub_part(ip[3], ip[4], (-1, 0), total_height, outer_mgn)

# part_height = total_height - bottom_height - 3
# part_length = 1
part_height = 3
part_length = 1
# 内側の辺に沿ってパーツを追加
box += create_sub_part(ip[7], ip[0], (1, 0), part_height, part_length)
box += create_sub_part(ip[0], ip[1], (0, -1), part_height, part_length)
box += create_sub_part(ip[1], ip[2], (-1, 0), part_height, part_length)
box += create_sub_part(ip[2], ip[3], (0, 1), part_height, part_length)
box += create_sub_part(ip[6], ip[7], (0, 1), part_height, part_length)
box.render()
# %%
# from solx import Cylinder

# cyl = Cylinder(radius=10,height=10)
# pt = pt3
# base_plate_solx += cyl.translate((pt[0], pt[1], 0))
base_plate.render()
dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
box.save_stl(f"{dst_dir_path}/box.stl")

# %%
mgn = 0.3
key_h = 15.0 + mgn
key_w = 15.0 + mgn

h = 5.0
inner_cube = Cube(size=(key_h, key_w, h))
outer_cube = Cube(size=(key_h + 2, key_w + 2, h))
dst = outer_cube - inner_cube
dst.render()
dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
dst.save_stl(f"{dst_dir_path}/key_box_{int(mgn*100)}.stl")

# %%
# outer_plate.render()
# # %%
# top_height = 0.5
# top_plate = SolxObject(linear_extrude(height=top_height)(
#     polygon(points=outer_points)
# ))

# def set_swith_diode(index: int, x: float, y: float):
#     global top_plate
#     inner_cube = Cube(size=(key_h, key_w, h))
#     inner_cube = inner_cube.translate((x, -y, 0))
#     top_plate -= inner_cube

# offset_x = 200
# offset_y = 100
# set_swith_diode(17, -23.0 + offset_x, -17.0 + offset_y)
# set_swith_diode(18, -23.0 + offset_x, 0.0 + offset_y)
# set_swith_diode(19, -23.0 + offset_x, 17.0 + offset_y)
# set_swith_diode(20, -23.0 + offset_x, 34.0 + offset_y)
# set_swith_diode(13, -40.0 + offset_x, -32.0 + offset_y)
# set_swith_diode(14, -40.0 + offset_x, -15.0 + offset_y)
# set_swith_diode(15, -40.0 + offset_x, 2.0 + offset_y)
# set_swith_diode(9, -57.0 + offset_x, -35.0 + offset_y)
# set_swith_diode(10, -57.0 + offset_x, -18.0 + offset_y)
# set_swith_diode(11, -57.0 + offset_x, -1.0 + offset_y)
# set_swith_diode(5, -74.0 + offset_x, -23.0 + offset_y)
# set_swith_diode(6, -74.0 + offset_x, -6.0 + offset_y)
# set_swith_diode(7, -74.0 + offset_x, 11.0 + offset_y)
# set_swith_diode(1, -91.0 + offset_x, -17.0 + offset_y)
# set_swith_diode(2, -91.0 + offset_x, 0.0 + offset_y)
# set_swith_diode(3, -91.0 + offset_x, 17.0 + offset_y)
# set_swith_diode(4, -108.0 + offset_x, 3.0 + offset_y)
# set_swith_diode(8, -108.0 + offset_x, 20.0 + offset_y)
# set_swith_diode(12, -109.0 + offset_x, 40.0 + offset_y)
# set_swith_diode(16, -92.0 + offset_x, 34.0 + offset_y)
# top_plate.render()
# top_plate.save_stl(f"{dst_dir_path}/top_plate.stl")
# # %%
