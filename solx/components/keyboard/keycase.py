# %%
from solx import Cube, Cylinder, HollowCube, PolygonExtrude, config
from solx.components.keyboard.arm_rest import ArmRest
from solx.components.keyboard.rubber_foot import RubberFoot
from solx.components.magnet.magnet_cylinder32 import MagnetCube32
from solx.components.screw.thread_nat import Nut, Screw
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
btm_h1 = 13.0
btm_h0 = 2.0

btm_out_mgn = 2.0
btm_pcb_mgn1 = 0.15
btm_pcb_mgn0 = 1.0

# top case layout
top_h0 = 2.0
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
bat_mgn_z = 5.0
bat_h = 4.0
bat_d = 12.0
bat_w = 5.0
bat_wall = 1.0

# mouse space
ms_right_mgn = 8.0
ms_plate_pcb_dz = 2.0
ms_plate_thin = 2.0
ms_scw_dx = 15.0
ms_scw_dy1 = 6.0
ms_scw_dy2 = 22.0
ms_scw_l = 2.0

# magnet
mag_dz = 3.0
mag_dy = 5.0

# calclate
btm_h = btm_h2 + btm_h1 + btm_h0
pcb2btm_out = btm_out_mgn + btm_pcb_mgn1
pcb2topout_xy = btm2top_out + pcb2btm_out
mouse_plate_z = btm_h0 + btm_h1 - ms_plate_pcb_dz





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

# mouse nearby area
mna_box = PolygonExtrude(
    points=[(pt.x, pt.y) for pt in btm_mouse_space.bottom_pts],
    height=mouse_plate.top_pts[0].z
)
btm_case += mna_box

# mag_top_right
mag_z = btm_h0 + btm_h1 - mag_dz
mag_y = pcb_out_pts[0][1] - mag_dy
mag_x_btm = btm_pts[0][0]
mag_x_top = top_subt_btm_pts[0][0]
cx = Cube((30, 1, 1),center=CenterType.CENTER)

mag_hole_cube = MagnetCube32()
mag_hole_cube_top = mag_hole_cube.rotate((0, -90, 0))
mag_hole_cube_top = mag_hole_cube_top.translate((mag_x_top, mag_y, mag_z))
mag_hole_cube_top = mag_hole_cube_top.translate((mag_hole_cube.h, 0, 0))
top_case = mag_hole_cube_top.add_to(top_case)
mag_hole_cube_btm = mag_hole_cube.rotate((0, 90, 0))
mag_hole_cube_btm = mag_hole_cube_btm.translate((mag_x_btm, mag_y, mag_z))
mag_hole_cube_btm = mag_hole_cube_btm.translate((-mag_hole_cube.h, 0, 0))
btm_case = mag_hole_cube_btm.add_to(btm_case)

##################
# arm rest bar
##################
cyl_h = 13
cyl_r = 2.5
v_bar_w = 3.0
v_bar_dd = 7.0
v_bar_h = cyl_r * 2
v_bar_dx = 45.0
v_bar_dz = 4.0

v_bar_d = btm2top_out + v_bar_dd + 2
v_bar = Cube(size=(v_bar_w, v_bar_d, v_bar_h))
v_bar_dy = btm_case.bottom_pts[2].y - v_bar_d / 2
v_bar = v_bar.translate((0, v_bar_dy, v_bar_dz))
dx = cyl_h/2 + v_bar_w / 2
base_bar = v_bar.translate((dx, 0, 0))
base_bar += v_bar.translate((-dx, 0, 0))
cyl_bar = Cylinder(radius=cyl_r, height=cyl_h)
cyl_bar = cyl_bar.rotate((0, 90, 0))
cyl_dy = v_bar_dy - v_bar_d / 2 + cyl_r
cyl_dz = v_bar_dz + v_bar_h / 2
cyl_bar = cyl_bar.translate((-cyl_h/2, cyl_dy, cyl_dz))
base_bar += cyl_bar
base_bar1 = base_bar.translate((v_bar_dx, 0, 0))
base_bar2 = base_bar.translate((-v_bar_dx, 0, 0))
btm_case += (base_bar1 + base_bar2)

##################
# arm rest
##################
arm_rest = ArmRest(
    plate_w = 110.0,
    plate_d = 130.0,
    plate_h = 2.0,
    plate_w2_ratio = 0.9,
    # slot cube
    cube_w = 10.0,
    cube_d = 5.0,
    cube_h = 5.0,
    cube_dx = 5.0,
    # slot ling
    bearing_outer_radius=cyl_r + 3.5,
    bearing_inner_radius=cyl_r + 0.5,
    bearing_height=cyl_h - 0.2,
    bearing_slot_width_narrow=cyl_r+2.0,
    bearing_slot_width_wide=cyl_r+3.5,
    bearing_slot_depth_wide=1.0,
    bearing_clearance_margin=0.3,
    bearing_wide_ty_rate=1/10
)
# arm_rest.slotted_bearing.inset.save_stl(config.EnvConfig.OUTPUT_STL_DIR_PATH + "/arm_rest_parts.stl")
# # arm_rest = arm_rest.rotate((180, 0, 0))
# # arm_rest = arm_rest.translate((0, -56, 18))
# # dst = btm_case + top_case + arm_rest
# # dst.render() 
# dst = arm_rest
# # LL = 1000
# # dst -= Cube(size=(LL, LL, LL), center=CenterType.CENTER).translate((LL/2, 0, 0))
# # dst -= Cube(size=(LL, LL, LL), center=CenterType.CENTER).translate((0, -LL/2 - 10, 0))
# # dst.render() 
# dst.save_stl(config.EnvConfig.OUTPUT_STL_DIR_PATH + "/arm_rest.stl")

# %%
##################
# foot
##################
nut_dz = 0.0
nat_h = 8.0
nut_dy = 40.0
t_mgn = 0.5
screw_height = 10 + nat_h - t_mgn - 0.2 - 2.5
screw_radius = 1.5
tooth_height = 0.8
tooth_width = 0.5
rotation_cnt = 5
handle_height = 3
handle_width = 35
handle_depth = 3
flat_ratio = 0.3
thread_front = Screw(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_radius,
    rotation_cnt=rotation_cnt,
    handle_height=handle_height,
    handle_width=handle_width,
    handle_depth=handle_depth,
    flat_ratio=flat_ratio,
)

nut_front = Nut(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_radius,
    rotation_cnt=rotation_cnt,
    nat_h=nat_h,
    tw_mgn=t_mgn,
    th_mgn=t_mgn,
    tr_mgn=t_mgn,
    nat_offset_xy=3
    )
thread_back = Screw(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_radius,
    rotation_cnt=rotation_cnt,
    handle_height=handle_height,
    handle_width=handle_width,
    handle_depth=handle_depth,
    flat_ratio=flat_ratio,
    inverse_thread_dicrection=True,
)
nut_back = Nut(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_radius,
    rotation_cnt=rotation_cnt,
    nat_h=nat_h,
    tw_mgn=t_mgn,
    th_mgn=t_mgn,
    tr_mgn=t_mgn,
    inverse_thread_dicrection=True,
    )
r_x = btm_case.bottom_pts[2].x
dz = nut_dz + nut_back.w / 2
nut_front = nut_front.rotate((0, -90, dz))
nut_back = nut_back.rotate((0, -90, dz))
nut_front = nut_front.translate((r_x, 0, dz))
nut_back = nut_back.translate((r_x, 0, dz))

nut_front = nut_front.translate((0, -nut_dy, 0))
nut_back = nut_back.translate((0, nut_dy, 0))
btm_case = nut_front.add_to(btm_case)
btm_case = nut_back.add_to(btm_case)
# %%
foot_hole_r = screw_radius + tooth_height + 0.1
foot = RubberFoot(
    screw_r=foot_hole_r,
    cylinder_r3=2.3,
    cylinder_h=14.0,
    cube_size=(10, 10, 36)
)
foot.save_stl(config.EnvConfig.OUTPUT_STL_DIR_PATH + "/rubber_foot.stl")
thread_front.save_stl(config.EnvConfig.OUTPUT_STL_DIR_PATH + "/thread_front.stl")
nut_front.save_stl(config.EnvConfig.OUTPUT_STL_DIR_PATH + "/nut_front.stl")
# %%
##################
# render
##################
RL = 200.0
dst_top = top_case.copy()
dst_btm = btm_case.copy()

offset_x = 0
offset_y = 0

dst_top = dst_top.translate((offset_x, offset_y, 0))
dst_btm = dst_btm.translate((offset_x, offset_y, 0))

is_subt_front = False
is_subt_back = False
is_subt_right = False
is_subt_left = False

# is_subt_front = True
is_subt_back = True
# is_subt_right = True
# is_subt_left = True

base_cube = Cube(size=(RL, RL, RL), center=CenterType.BOTTOM_CENTER)
# 手前を引く
if is_subt_front:
    front_cube = base_cube.translate((0, - RL / 2, 0))
    dst_top -= front_cube
    dst_btm -= front_cube
# 奥を引く
if is_subt_back:
    back_cube = base_cube.translate((0, RL / 2, 0))
    dst_top -= back_cube
    dst_btm -= back_cube
# 右を引く
if is_subt_right:
    s_cube = base_cube.translate((RL / 2, 0, 0))
    dst_top -= s_cube
    dst_btm -= s_cube
# # 左を引く
if is_subt_left:
    s_cube = base_cube.translate((-RL / 2, 0, 0))
    dst_top -= s_cube
    dst_btm -= s_cube

dst_dir_path = config.EnvConfig.OUTPUT_STL_DIR_PATH
(dst_top + dst_btm).render()
dst_top.save_stl(dst_dir_path + "/top_case.stl")
dst_btm.save_stl(dst_dir_path + "/btm_case.stl")

# %%
