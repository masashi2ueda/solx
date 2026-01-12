# %%
from solx import Cube, Cylinder, HollowCube, PolygonExtrude
from solx.primitives.types import CenterType

LARGE_VAL = 100
##### case point layout
#  ↑y
# →x
# pt1-------------------pt0
#  |                     |
#  |   pt4-----pt5       |
# pt2--pt3     pt6------pt7
btm_h2 = 2.0
btm_h1 = 10.0
btm_h0 = 0.5

btm_out_mgn = 1.0
btm_pcb_mgn1 = 0.15
btm_pcb_mgn0 = 1.0

# top case layout
top_h0 = 1.0
top_h1 = 6.0
btm_top_mgn_xy = 0.15
top_out_mgn = 3.0
btm2top_out = btm_top_mgn_xy + top_out_mgn

# top case around micon
top_micon_wall = 1.0
top_micon_dh = 4 + top_micon_wall
top_micon_dw = 22.0
top_micon_dd = 25.0

# usb
usb_cnt_x = 11.0
usb_w = 17.0
usb_top_z = 8.0

# battery switch space
bat_mgn_y = 30.0
bat_mgn_z = 2.0
bat_h = 4.0
bat_d = 10.0
bat_w = 5.0
bat_wall = 1.0

# mouse space
ms_right_mgn = 8.0
ms_plate_pcb_dz = 1.0
ms_plate_thin = 2.0
ms_scw_dx = 15.0
ms_scw_dy1 = 6.0
ms_scw_dy2 = 22.0
ms_scw_l = 2.0


# calclate
btm_h = btm_h2 + btm_h1 + btm_h0
pcb2btm_out = btm_out_mgn + btm_pcb_mgn1
pcb2topout_xy = btm2top_out + pcb2btm_out
mouse_plate_z = btm_h0 + btm_h1





def shift_pcb_points(pts, mgn):
    outer_direstion = [
        ( +1, +1),  # pt0
        ( -1, +1),  # pt1
        ( -1, -1),  # pt2
        ( +1, -1),  # pt3
        ( +1, -1),  # pt4
        ( -1, -1),  # pt5
        ( -1, -1),  # pt6
        ( +1, -1),  # pt7
    ]
    dst_points = [
        (
            pts[i][0] + outer_direstion[i][0] * mgn,
            pts[i][1] + outer_direstion[i][1] * mgn)
        for i in range(len(pts))
    ]
    return dst_points

# R
pcb_out_pts_raw = [(189.0, 55.0), (77.0, 55.0), (77.0, 150.0), (118.0, 150.0), (118.0, 121.0), (158.895, 121.0), (158.895, 150.0), (189.0, 150.0)]

##################
# bottom case
##################
# pcb points
pcb_out_pts = [(x, -y) for x, y in pcb_out_pts_raw]
cx = pcb_out_pts[1][0] / 2 + pcb_out_pts[0][0] / 2
cy = pcb_out_pts[2][1] / 2 + pcb_out_pts[1][1] / 2
pcb_out_pts = [(x - cx, y - cy) for x, y in pcb_out_pts]

# pcb_plate
pcb_plate = PolygonExtrude(points=pcb_out_pts, height=2)
pcb_plate = pcb_plate.translate((0, 0, btm_h0 + btm_h1))

# bottom case outer cube
btm_pts = shift_pcb_points(pcb_out_pts, pcb2btm_out)
btm_case = PolygonExtrude(points=btm_pts,height=btm_h)

# for battery space
btm_bat_space_pts = shift_pcb_points(pcb_out_pts, -btm_pcb_mgn0)
btm_bat_space = PolygonExtrude(points=btm_bat_space_pts, height=btm_h1 + btm_h2)
btm_bat_space = btm_bat_space.translate((0, 0, btm_h0))
btm_case -= btm_bat_space

# for pcb space
btm_pcb_space_pts = shift_pcb_points(pcb_out_pts, btm_pcb_mgn1)
btm_pcb_space = PolygonExtrude(points=btm_pcb_space_pts,height=btm_h2)
btm_pcb_space = btm_pcb_space.translate((0, 0, btm_h0 + btm_h1))
btm_case -= btm_pcb_space

# for mouse space
btm_ms_mgn = pcb2btm_out + btm_pcb_mgn0
btm_ms_x = btm_pts[5][0]
btm_ms_y0 = btm_pts[5][1] + btm_ms_mgn
btm_ms_y1 = btm_pts[6][1]
btm_mouse_pts = [
    (btm_ms_x, btm_ms_y0),
    (btm_ms_x, btm_ms_y1),
    (btm_ms_x + btm_ms_mgn, btm_ms_y1),
    (btm_ms_x + btm_ms_mgn, btm_ms_y0)
]
btm_mouse_space = PolygonExtrude(points=btm_mouse_pts,height=btm_h2+btm_h1+btm_h0)
btm_case -= btm_mouse_space

# (btm_case).render()

##################
# top case
##################
# top case
top_points = shift_pcb_points(btm_pts, btm2top_out)
top_h = btm_h + top_h0
top_case = PolygonExtrude(points=top_points,height=top_h)

# subtract bottom case space
top_subt_btm_pts = shift_pcb_points(btm_pts, btm_top_mgn_xy)
sbt_btm_case = PolygonExtrude(points=top_subt_btm_pts,height=btm_h)
top_case -= sbt_btm_case

# subtract half h
sbt_btm_case = PolygonExtrude(points=top_points,height=btm_h - top_h1)
top_case -= sbt_btm_case


# around micon
cw = top_micon_dw + pcb2topout_xy + top_micon_wall
cd = top_micon_dd + pcb2topout_xy
ch = top_h0 + top_micon_dh
mcn_add_box = HollowCube(
    size=(cw, cd, ch),
    wall_thickness=top_micon_wall,
    d_mz=-top_h0, # no bottom wall
    d_py=top_out_mgn, d_mx = top_out_mgn, # side wall
    center=CenterType.BOTTOM_LEFT)
mcn_add_box = mcn_add_box.translate(
    (top_points[1][0], top_points[1][1] - cd, btm_h))
top_case = mcn_add_box.add_to(top_case)

# subtract usb space
usb_h = btm_h + usb_top_z
usb_cube_size = (usb_w, top_out_mgn, usb_h)
usb_obj = Cube(size=usb_cube_size, center=CenterType.BOTTOM_CENTER)
usb_obj = usb_obj.translate((
    pcb_out_pts[1][0] + usb_cnt_x,
    top_points[1][1] - usb_cube_size[1]/2,
    0
))
top_case -= usb_obj

# around battery switch
bsw_d = bat_d
bsw_w = bat_w + pcb2topout_xy
bsw_h = bat_mgn_z
org_x = pcb_out_pts[2][0] - pcb2topout_xy + bsw_w / 2
org_y = pcb_out_pts[2][1] + bat_mgn_y
org_z = btm_h
bsw_c = HollowCube(
    size=(bsw_w, bsw_d, bsw_h),
    wall_thickness=bat_wall,
    d_mx = 0, # no left wall
    d_mz = - top_h1, # no bottom wall
    center=CenterType.BOTTOM_CENTER
)
bsw_c = bsw_c.translate((org_x, org_y, org_z))
top_case = bsw_c.add_to(top_case)

# key switch spae
def set_swith_diode(index: int, x: float, y: float):
    global top_case, cx, cy
    mgn = 0.3
    key_h = 15.0 + mgn
    key_w = 15.0 + mgn
    inner_cube = Cube(size=(key_h, key_w, 100))
    inner_cube = inner_cube.translate((x - cx, -y - cy, 0))
    top_case -= inner_cube
offset_x = 200
offset_y = 100
set_swith_diode(17, -23.0 + offset_x, -17.0 + offset_y)
set_swith_diode(18, -23.0 + offset_x, 0.0 + offset_y)
set_swith_diode(19, -23.0 + offset_x, 17.0 + offset_y)
set_swith_diode(20, -23.0 + offset_x, 34.0 + offset_y)
set_swith_diode(13, -40.0 + offset_x, -32.0 + offset_y)
set_swith_diode(14, -40.0 + offset_x, -15.0 + offset_y)
set_swith_diode(15, -40.0 + offset_x, 2.0 + offset_y)
set_swith_diode(9, -57.0 + offset_x, -35.0 + offset_y)
set_swith_diode(10, -57.0 + offset_x, -18.0 + offset_y)
set_swith_diode(11, -57.0 + offset_x, -1.0 + offset_y)
set_swith_diode(5, -74.0 + offset_x, -23.0 + offset_y)
set_swith_diode(6, -74.0 + offset_x, -6.0 + offset_y)
set_swith_diode(7, -74.0 + offset_x, 11.0 + offset_y)
set_swith_diode(1, -91.0 + offset_x, -17.0 + offset_y)
set_swith_diode(2, -91.0 + offset_x, 0.0 + offset_y)
set_swith_diode(3, -91.0 + offset_x, 17.0 + offset_y)
set_swith_diode(4, -108.0 + offset_x, 3.0 + offset_y)
set_swith_diode(8, -108.0 + offset_x, 20.0 + offset_y)
set_swith_diode(12, -109.0 + offset_x, 40.0 + offset_y)
set_swith_diode(16, -92.0 + offset_x, 34.0 + offset_y)


# subtract mouse space
right_mx = pcb_out_pts[5][0] + ms_right_mgn
left_mx = pcb_out_pts[4][0]
up_my = pcb_out_pts[5][1]
down_my = top_points[6][1]
ms_pt0 = (right_mx, up_my)
ms_pt1= (left_mx, up_my)
ms_pt2= (left_mx, down_my)
ms_pt3 = (right_mx, down_my)
mouse_subt_cube = PolygonExtrude(
    points=[ms_pt0, ms_pt1, ms_pt2, ms_pt3],
    height=LARGE_VAL
)
top_case -= mouse_subt_cube.translate((0, 0, 0))
btm_case -= mouse_subt_cube.translate((0, 0, mouse_plate_z))

# mouse plate
right_mx = pcb_out_pts[5][0]
left_mx = pcb_out_pts[4][0]
up_my = pcb_out_pts[5][1]
down_my = pcb_out_pts[6][1]
ms_pt0 = (right_mx, up_my)
ms_pt1= (left_mx, up_my)
ms_pt2= (left_mx, down_my)
ms_pt3 = (right_mx, down_my)
mouse_plate = PolygonExtrude(
    points=[ms_pt0, ms_pt1, ms_pt2, ms_pt3],
    height=ms_plate_thin
).translate((0, 0, mouse_plate_z - ms_plate_thin))
# screw hole
screw_hole = Cylinder(radius=ms_scw_l / 2, height=ms_plate_thin)
hl_x = right_mx - ms_scw_dx
hl_z = mouse_plate_z - ms_plate_thin
mouse_plate -= screw_hole.translate((hl_x, down_my + ms_scw_dy1, hl_z))
mouse_plate -= screw_hole.translate((hl_x, down_my + ms_scw_dy2, hl_z))
btm_case += mouse_plate


# mag_top_right
mag_dz = 3.0
mag_dy = 5.0
mag_z = btm_h0 + btm_h1 - mag_dz
mag_y = pcb_out_pts[0][1] - mag_dy
mag_x_btm = btm_pts[0][0]
mag_x_top = top_subt_btm_pts[0][0]
cx = Cube((30, 1, 1),center=CenterType.CENTER)
from solx.components.magnet.magnet_cylinder32 import MagnetCube32

mag_hole_cube = MagnetCube32()
mag_hole_cube_top = mag_hole_cube.rotate((0, -90, 0))
mag_hole_cube_top = mag_hole_cube_top.translate((mag_x_top, mag_y, mag_z))
mag_hole_cube_top = mag_hole_cube_top.translate((mag_hole_cube.h, 0, 0))
top_case = mag_hole_cube_top.add_to(top_case)
mag_hole_cube_btm = mag_hole_cube.rotate((0, 90, 0))
mag_hole_cube_btm = mag_hole_cube_btm.translate((mag_x_btm, mag_y, mag_z))
mag_hole_cube_btm = mag_hole_cube_btm.translate((-mag_hole_cube.h, 0, 0))
btm_case = mag_hole_cube_btm.add_to(btm_case)

# mag_cyl_l0 = mag_cyl.copy()
# mag_cyl_r0 = mag_cyl.translate((-mc32.h, 0, 0))
# dst += cx.translate((mag_x_btm, mag_y, mag_z))
# dst += mag_cyl_r0
# dst -= mag_cyl_r0.translate((mag_x_btm, mag_y, mag_z))
# dst -= mag_cyl_l0.translate((mag_x_top, mag_y, mag_z))


##################
# render
##################
# render
dst = btm_case + top_case
# dst = top_case
# dst = btm_case
# subt up right
subt_cube = Cube(size=(LARGE_VAL, LARGE_VAL, LARGE_VAL), center=CenterType.BOTTOM_LEFT)
# subt down right
subt_cube = subt_cube.translate((0, -LARGE_VAL, 0))
(dst - subt_cube).render()

# %%

large_val = 10.0
min_val = 0.1


######################################
# bottom case usb space
######################################
#               btm_usb_offset_x
#               ←-→
#              |   (   )
# pcb_left_up →|_________↕ btm_usb_offset_z
btm_usb_offset_x = 7
btm_usb_offset_z = 3

######################################
# bottom case battery space
######################################
#               bat_usb_offset_y
#               ←-→
#              |   (   )
# pcb_left_up →|_________↕ bat_usb_offset_z
######################################
bat_usb_offset_y = 63
bat_usb_offset_z = 2


######################################
# top case layout
#####################################
#             (top case)
#             __________________
#             |oo ______________↨ top_h0
#             |oo|  _________________
#    top_h1↨  |oo| |xxxxx(bottom case)
#              ---↔ btm_top_mgn_xy
#             <->: top_out_mgn
top_h0 = 1.0
top_h1 = 6.0
btm_top_mgn_xy = 0.15
top_out_mgn = 3.0

######################################
# top case around micon
#####################################
top_micon_wall = 1.0
top_micon_dh = 4 + top_micon_wall
top_micon_dw = 22.0
top_micon_dd = 25.0

######################################
# usb
#####################################
usb_cnt_x = 11.0
usb_w = 17.0
usb_top_z = 8.0
# usb_h = 12.0


######################################
# battery switch space
#####################################
bat_mgn_y = 30.0
bat_mgn_z = 2.0
bat_h = 4.0
bat_d = 10.0
bat_w = 5.0




# %%





# (btm_case + pcb_plate).render()





pcb2topout_xy = top_out_mgn + btm_top_mgn_xy + btm_out_mgn + btm_pcb_mgn1
btm2pcbtop = btm_h0 + btm_h1 + btm_h2











# %%
dst = btm_case
# dst = top_case
# dst = btm_case + top_case

# mag_top_right
mag_z = btm_h0 + btm_h1 - 2.0
mag_dy = 5.0
mag_y = pcb_out_pts[0][1] - mag_dy
mag_x_btm = btm_pts[0][0]
mag_x_top = top_subt_btm_pts[0][0]
cx = Cube((30, 1, 1),center=CenterType.CENTER)
from solx.components.magnet import magnet_cylinder32 as mc32

mag_hole_cube = mc32.MagnetHoleCube()
# mag_cyl = mag_cyl.rotate((0, 90, 0))
dst += mag_hole_cube
# mag_cyl_l0 = mag_cyl.copy()
# mag_cyl_r0 = mag_cyl.translate((-mc32.h, 0, 0))
# dst += cx.translate((mag_x_btm, mag_y, mag_z))
# dst += mag_cyl_r0
# dst -= mag_cyl_r0.translate((mag_x_btm, mag_y, mag_z))
# dst -= mag_cyl_l0.translate((mag_x_top, mag_y, mag_z))


only_type = ""
# only_type = "left_top"
# only_type = "down"
only_type = "top"
# only left top
if only_type == "left_top":
    off_cube = Cube(size=(150, 180, 30), center=CenterType.BOTTOM_LEFT)
    dst -= off_cube.translate((98, -160, 0))
    dst -= off_cube.translate((50, -250, 0))
# only left down
if only_type == "left_down":
    off_cube = Cube(size=(150, 180, 30), center=CenterType.BOTTOM_LEFT)
    dst -= off_cube.translate((110, -160, 0))
    dst -= off_cube.translate((50, -100, 0))
if only_type == "down":
    off_cube = Cube(size=(150, 180, 30), center=CenterType.BOTTOM_LEFT)
    dst -= off_cube.translate((50, -100, 0))
if only_type == "top":
    off_cube = Cube(size=(150, 180, 30), center=CenterType.BOTTOM_LEFT)
    dst -= off_cube.translate((50, -250, 0))

dst.render()
dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
dst.save_stl(f"{dst_dir_path}/case.stl")
dst.save_scad(f"{dst_dir_path}/case.scad")

# %%


# %%
btm_outer_case.render()
# %%

cube = Cube(size=(10, 10, 10))
cylinder1 = Cylinder(radius=5, height=10)
cylinder2 = Cylinder(radius=5, height=10)
dst = cube + cylinder1.translate((5, 0, 0)) + cylinder2.translate((-5, 0, 0))
dst.render()
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
