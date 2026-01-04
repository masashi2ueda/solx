# %%
from solx import Cube, Cylinder, HollowCube, PolygonExtrude
from solx.components.magnet import magnet_cylinder32
from solx.primitives.types import CenterType

large_val = 10.0
min_val = 0.1

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
top_h1 = 5.0
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

# R
pcb_out_pts_raw = [(189.0, 55.0), (77.0, 55.0), (77.0, 150.0), (118.0, 150.0), (118.0, 121.0), (158.895, 121.0), (158.895, 150.0), (189.0, 150.0)]


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


# %%
##################
# base bottom case
##################
# Invert Y axis
pcb_out_pts = [(x, -y) for x, y in pcb_out_pts_raw]

pcb_plate = PolygonExtrude(points=pcb_out_pts, height=2)
pcb_plate = pcb_plate.translate((0, 0, btm_h0 + btm_h1))

# bottom case outer cube
btm_case = PolygonExtrude(
    points=shift_pcb_points(pcb_out_pts, btm_out_mgn),
    height=btm_h2 + btm_h1 + btm_h0
)

# for battery space
btm_case -= PolygonExtrude(
    points=shift_pcb_points(pcb_out_pts, -btm_pcb_mgn0),
    height=btm_h1 + btm_h2
).translate((0, 0, btm_h0))

# for pcb space
btm_case -= PolygonExtrude(
    points=shift_pcb_points(pcb_out_pts, btm_pcb_mgn1),
    height=btm_h2
).translate((0, 0, btm_h0+btm_h1))

# subtract mouse space
ms_org_pt5x = pcb_out_pts[5][0]
ms_org_pt5y = pcb_out_pts[5][1]
ms_org_pt6x = pcb_out_pts[6][0]
ms_org_pt6y = pcb_out_pts[6][1]
ms_pt0 = (ms_org_pt5x+btm_pcb_mgn0, ms_org_pt5y+btm_pcb_mgn0)
ms_pt1= (ms_org_pt5x-btm_out_mgn, ms_org_pt5y+btm_pcb_mgn0)
ms_pt2= (ms_org_pt6x-btm_out_mgn, ms_org_pt6y-btm_pcb_mgn0)
ms_pt3 = (ms_org_pt6x+btm_pcb_mgn0, ms_org_pt6y-btm_pcb_mgn0)
btm_case -= PolygonExtrude(
    points=[ms_pt0, ms_pt1, ms_pt2, ms_pt3],
    height=btm_h2+btm_h1+btm_h0
)

(btm_case + pcb_plate).render()

# %%
# top case
top_points = shift_pcb_points(
    pcb_out_pts,
    top_out_mgn + btm_top_mgn_xy + btm_out_mgn + btm_pcb_mgn1)
btm_h = btm_h2 + btm_h1 + btm_h0
top_case = PolygonExtrude(
    points=top_points,
    height=btm_h + top_h0
)

# subtract bottom case space
sbt_btm_case = PolygonExtrude(
    points=shift_pcb_points(pcb_out_pts,
    btm_top_mgn_xy + btm_out_mgn + btm_pcb_mgn1),
    height=btm_h
)
top_case -= sbt_btm_case

# subtract half h
sbt_btm_case = PolygonExtrude(
    points=shift_pcb_points(pcb_out_pts,
    btm_out_mgn+large_val),
    height=btm_h - top_h1
)
top_case -= sbt_btm_case

pcb2topout_xy = top_out_mgn + btm_top_mgn_xy + btm_out_mgn + btm_pcb_mgn1
btm2pcbtop = btm_h0 + btm_h1 + btm_h2

# around micon
mcn_org_x = pcb_out_pts[1][0] - pcb2topout_xy
mcn_org_y = pcb_out_pts[1][1] + pcb2topout_xy
mcn_org_z = btm_h0 + btm_h1 + btm_h2
cw = top_micon_dw + pcb2topout_xy + top_micon_wall
cd = top_micon_dd + pcb2topout_xy
ch = top_h0 + top_micon_dh
mcn_sbt_box = Cube(size=(cw, cd, ch),center=CenterType.BOTTOM_LEFT)
mcn_sbt_box = mcn_sbt_box.translate((mcn_org_x, mcn_org_y - cd, mcn_org_z))
top_case -= mcn_sbt_box
mcn_add_box = HollowCube(
    size=(cw, cd, ch),
    wall_thickness=top_micon_wall,
    d_mz=0, # no bottom wall
    d_py=top_out_mgn, d_mx = top_out_mgn, # side wall
    center=CenterType.BOTTOM_LEFT)
mcn_add_box = mcn_add_box.translate((mcn_org_x,mcn_org_y - cd,mcn_org_z))
top_case += mcn_add_box

# subtract usb space
usb_dd = 2
usb_h = btm2pcbtop + usb_top_z
usb_cube_size = (
    usb_w,
    top_out_mgn + usb_dd,
    usb_h)
usb_obj = Cube(size=usb_cube_size, center=CenterType.BOTTOM_CENTER)
usb_obj = usb_obj.translate((
    pcb_out_pts[1][0] + usb_cnt_x,
    top_points[1][1] - usb_cube_size[1]/2 + usb_dd / 2,
    0
))
top_case -= usb_obj
# top_case -= usb_obj.translate((0, 0, -usb_dd/2))


# # around battery
# clr = 1.0
# pcb2out_mgn = top_out_mgn + btm_top_mgn_xy + btm_out_mgn + btm_pcb_mgn1
# bat_cube_w = pcb2out_mgn + bat_w + clr
# bat_cube_d = bat_d + clr * 2
# bat_cube_h = bat_mgn_z + bat_h / 2 + clr
# bat_sbt_cube = Cube(size=(bat_cube_w, bat_cube_d, bat_cube_h), center=CenterType.BOTTOM_CENTER)
# bat_org_x = pcb_out_pts[2][0] - pcb2out_mgn
# bat_org_y = pcb_out_pts[2][1] + bat_mgn_y
# top_case += bat_sbt_cube

# # subtract battery space
# bat_cube_size = (10.0, 5.0, btm_out_mgn + btm_pcb_mgn1 + btm_pcb_mgn0)
# bat_obj = RoundedCube(size=bat_cube_size, radius=1.0)
# bat_obj = bat_obj.rotate((90, 0, 0)).rotate((0, 0, 90))
# bat_obj = bat_obj.translate((0,-bat_cube_size[0]/2,0))
# bat_obj = bat_obj.translate((
#     pcb_out_pts[1][0] - btm_out_mgn - 0.1,
#     pcb_out_pts[1][1] - bat_usb_offset_y,
#     btm_h0 + btm_h1 + bat_usb_offset_z
# ))
# btm_case -= bat_obj
# top_case += pcb_plate
# (top_case + pcb_plate).render()
top_case.render()
mag_cylinder = magnet_cylinder32.create_magnet_hole()
# %%
# dst = btm_case
dst = top_case
# dst = btm_case + top_case
# only_type = ""
only_type = "left_top"
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
dst.render()
dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
dst.save_stl(f"{dst_dir_path}/case.stl")

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
