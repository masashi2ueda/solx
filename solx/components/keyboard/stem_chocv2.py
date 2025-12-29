# %%
"""Choc v2 switch stem with cross-shaped slots."""
from solx import CenterType, Cube, Cylinder

MGN = 0.25 # 22~24がよい
def create_chocv2_stem(inverted=False):
    """Create a Choc v2 switch stem with cross-shaped slots.

    Choc v2 stems have specific dimensions:
    - Diameter: approximately 4.0mm (radius 2.0mm)
    - Height: approximately 3.4mm
    - Cross slots for keycap attachment: 1.2mm wide, extending from center

    Args:
        inverted (bool): If True, creates an inverted stem (upside down)

    Returns:
        SolxObject: The Choc v2 stem with cross slots
    """
    # Main stem cylinder
    # Choc v2 stem diameter is approximately 4.0mm, height is about 3.4mm
    stem_height = 6.5
    stem_radius = (5.8 - MGN) / 2
    stem_cylinder = Cylinder(
        # radius=2.0,  # 4.0mm diameter
        # height=3.4,  # Standard Choc v2 stem height
        radius=stem_radius,  # 5.8mm diameter
        height=stem_height,  # Standard Choc v2 stem height
        center=CenterType.BOTTOM_CENTER
    )

    # Cross slot dimensions
    # mgn = 0.15
    # slot_width = 1.2 + mgn # Width of each slot arm
    # slot_length = 3.5 + mgn # Length of each slot (slightly longer than diameter)
    # slot_height = 3.5 + mgn + 0.2 # Height to fully cut through the stem
    slot_width = 1.3 + MGN # Width of each slot arm
    slot_length = 4.2 + MGN # Length of each slot (slightly longer than diameter)
    slot_height = 5.0 + MGN # Height to fully cut through the stem

    # Create the two perpendicular rectangular slots for the cross
    # Horizontal slot (along X-axis)
    horizontal_slot = Cube(
        width=slot_length,
        depth=slot_width,
        height=slot_height,
        center=CenterType.BOTTOM_CENTER
    )

    # Vertical slot (along Y-axis)
    vertical_slot = Cube(
        width=slot_width,
        depth=slot_length,
        height=slot_height,
        center=CenterType.BOTTOM_CENTER
    )

    # Move slots to the center of the stem (at height 1.7mm from bottom)
    horizontal_slot_positioned = horizontal_slot
    vertical_slot_positioned = vertical_slot

    # Create the cross slot by combining the two perpendicular slots using + operator
    cross_slot = horizontal_slot_positioned + vertical_slot_positioned

    # Subtract the cross slot from the cylinder using - operator
    stem_with_slots = stem_cylinder - cross_slot

    # If inverted, rotate 180 degrees around X-axis
    if inverted:
        stem_with_slots = stem_with_slots.rotate_x(180).translate((0, 0, 3.4))
        stem_with_slots = stem_with_slots.translate((0, 0, stem_height / 2))

    return stem_with_slots

# %%
if __name__ == "__main__":
    dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
    stem = create_chocv2_stem(inverted=True)
    stem.save_stl(f"{dst_dir_path}/chocv2_stem{int(MGN*100)}.stl")

# %%
