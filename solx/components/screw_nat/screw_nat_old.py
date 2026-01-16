# %%
import solid

from solx.core import SolxObject

th = solid.screw_thread.thread()
th = SolxObject(th)
th.render()

# %%
from __future__ import annotations

from typing import TypeVar

from solx.core import SolxObject

T = TypeVar("T", bound=SolxObject)


# %%
from solid import (
    cylinder,
    difference,
    linear_extrude,
    polygon,
    scad_render_to_file,
    translate,
    union,
)


def thread(
    length=20,
    pitch=2,
    major_radius=5,
    minor_radius=4,
    fn=64,
):
    """
    簡易ねじ山
    """
    height = length
    turns = height / pitch
    twist = 360 * turns

    # ねじ断面（三角形）
    tooth_height = major_radius - minor_radius
    tooth_width = pitch * 0.6

    tooth = polygon([
        [0, 0],
        [tooth_width / 2, tooth_height],
        [-tooth_width / 2, tooth_height],
    ])

    return (
        translate([major_radius, 0, 0])(
            linear_extrude(
                height=height,
                twist=twist,
                slices=int(turns * fn),
                scale=1,
            )(tooth)
        )
    )

def bolt(
    length=20,
    pitch=2,
    major_radius=5,
    minor_radius=4,
):
    core = cylinder(
        h=length,
        r=minor_radius,
        segments=64
    )

    threads = thread(
        length=length,
        pitch=pitch,
        major_radius=major_radius,
        minor_radius=minor_radius,
    )

    head = translate([0, 0, length])(
        cylinder(h=4, r=major_radius * 1.2, segments=6)
    )

    return union()(
        core,
        threads,
        head
    )

def nut(
    thickness=6,
    pitch=2,
    major_radius=5,
    minor_radius=4,
    clearance=0.3,  # 3Dプリント用クリアランス
):
    outer = cylinder(
        h=thickness,
        r=major_radius * 1.4,
        segments=6
    )

    hole_core = cylinder(
        h=thickness,
        r=minor_radius + clearance,
        segments=64
    )

    hole_threads = thread(
        length=thickness,
        pitch=pitch,
        major_radius=major_radius + clearance,
        minor_radius=minor_radius + clearance,
    )

    return difference()(
        outer,
        hole_core,
        hole_threads
    )

bolt = bolt()
# model = union()(
#     bolt(),
#     translate([0, 0, -6])(nut())
# )

scad_render_to_file(
    bolt,
    filepath="/home/uedam/dev/solx/examples/output_stl/bolt_and_nut.scad",
    file_header="$fn=64;"
)

# %%
