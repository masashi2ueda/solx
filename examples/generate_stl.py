# %%
"""
"""

import os

from solx.components.keyboard.stem_chocv2 import create_chocv2_stem

# 出力ディレクトリを作成
output_dir = "output_stl"
os.makedirs(output_dir, exist_ok=True)

chocv2_stem = create_chocv2_stem()
chocv2_stem.save_stl(os.path.join(output_dir, "chocv2_stem.stl"))

# %%
