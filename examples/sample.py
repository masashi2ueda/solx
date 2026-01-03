# %%
import solid
from viewscad import Renderer

import solx
from solx.config.openscad import get_openscad_path

# %%
# Initialize renderer with configured OpenSCAD path
renderer = Renderer(
    openscad_path=get_openscad_path(),
)

cube = solid.cube(size=10)
cube = solid.color([1, 0, 0, 0.1])(cube)


renderer.render(cube)
solid.scad_render_to_file(cube, f"{solx.EnvConfig.OUTPUT_STL_DIR_PATH}/output.scad")


# %%
