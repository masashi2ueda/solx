# %%
"""Choc v2 switch stem with cross-shaped slots."""
from solx import CenterType, Cylinder


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
    stem_cylinder = Cylinder(
        radius=2.0,  # 4.0mm diameter
        height=3.4,  # Standard Choc v2 stem height
        center=CenterType.BOTTOM_CENTER
    )

    # Cross slot dimensions
    mgn = 0.15
    slot_width = 1.2 + mgn # Width of each slot arm
    slot_length = 3.5 + mgn # Length of each slot (slightly longer than diameter)
    slot_height = 3.5 + mgn # Height to fully cut through the stem

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
    horizontal_slot_positioned = horizontal_slot.translate((0, 0, 1.7))
    vertical_slot_positioned = vertical_slot.translate((0, 0, 1.7))

    # Create the cross slot by combining the two perpendicular slots using + operator
    cross_slot = horizontal_slot_positioned + vertical_slot_positioned

    # Subtract the cross slot from the cylinder using - operator
    stem_with_slots = stem_cylinder - cross_slot

    # If inverted, rotate 180 degrees around X-axis
    if not inverted:
        stem_with_slots = stem_with_slots.rotate_x(180).translate((0, 0, 3.4))

    return stem_with_slots

# %%
