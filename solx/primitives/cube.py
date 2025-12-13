# %%
import viewscad

from solx import SolxObject
from solid import cube

openscad_exec = "/usr/bin/openscad"


def get_render():
    return viewscad.Renderer(openscad_exec=openscad_exec)


# %%
c = cube(10)
so = SolxObject(c)
so.render()
# r = get_render()
# r.render(c)

# %%
