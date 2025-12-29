# %%
from solx import Cube, PolygonExtrude

#####################################
##### case point layout
#  ↑y
# →x
# pt1-------------------pt0
#  |                     |
#  |   pt4-----pt5       |
# pt2--pt3     pt6------pt7
#
### bottom case z axis layout
# xx↕btm_h2(pcb + xiao ble)
# xxx↕btm_h1(battery space)
# xxxxxx↕btm_h0
#
### bottom case xy axis layout
#
# |←--→| : btm_out_mgn
# |xxxx|↔|(pcb): btm_pcb_mgn1
#        |←-→|: btm_pcb_mgn0
# |xxxxxxxxxx|
# |xxxxxxxxxxxxxxxxxx
######################################

large_val = 10.0
btm_h2 = 8.0
btm_h1 = 10.0
btm_h0 = 0.5

btm_out_mgn = 1.0
btm_pcb_mgn1 = 0.15
btm_pcb_mgn0 = 1.0

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

# ms_pt0 = (pcb_out_pts[5][0] + btm_pcb_mgn0, pcb_out_pts[5][1] - btm_out_mgn-btm_pcb_mgn0-btm_pcb_mgn1)
# ms_pt1 = (pcb_out_pts[5][0] - btm_out_mgn, pcb_out_pts[5][1] - btm_out_mgn-btm_pcb_mgn0-btm_pcb_mgn1)
# ms_pt2 = (pcb_out_pts[6][0] - btm_out_mgn, pcb_out_pts[6][1] + btm_out_mgn)
# ms_pt3 = (pcb_out_pts[6][0] + btm_out_mgn, pcb_out_pts[6][1] + btm_out_mgn)
ms_pt0 = (ms_org_pt5x+btm_pcb_mgn0, ms_org_pt5y+btm_pcb_mgn0)
# x = ms_pt0[0]
# y = ms_pt0[1]
# btm_case += Cube(size=(0.5, 0.5, 30)).translate((x, y, 0))

ms_pt1= (ms_org_pt5x-btm_out_mgn, ms_org_pt5y+btm_pcb_mgn0)
# x = ms_pt1[0]
# y = ms_pt1[1]
# btm_case += Cube(size=(0.5, 0.5, 30)).translate((x, y, 0))

ms_pt2= (ms_org_pt6x-btm_out_mgn, ms_org_pt6y-btm_pcb_mgn0)
# x = ms_pt2[0]
# y = ms_pt2[1]
# btm_case += Cube(size=(0.5, 0.5, 30)).translate((x, y, 0))

ms_pt3 = (ms_org_pt6x+btm_pcb_mgn0, ms_org_pt6y-btm_pcb_mgn0)
# x = ms_pt3[0]
# y = ms_pt3[1]
# btm_case += Cube(size=(0.5, 0.5, 30)).translate((x, y, 0))

btm_case -= PolygonExtrude(
    points=[ms_pt0, ms_pt1, ms_pt2, ms_pt3],
    height=btm_h2+btm_h1+btm_h0
)


btm_case.render()


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
