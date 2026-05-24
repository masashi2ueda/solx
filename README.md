# solx
An extended API for SolidPython and OpenSCAD.

## Prerequisites

This package requires OpenSCAD to be installed on your system.

This package also requires `setuptools<82` due to compatibility constraints.
If needed, install it explicitly before installing `solx`:

```bash
uv add "setuptools<82"
```

### Installing OpenSCAD

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openscad
```

**macOS:**
```bash
brew install openscad
```

**Windows:**
Download and install from [OpenSCAD official website](https://openscad.org/downloads.html)

## 3D Printable Assets

Ready-to-print STL files are available separately to keep the pip package lightweight:

- **Download**: Get STL files from [Releases](releases) 
- **Location**: Place STL files in `assets/stl/` directory
- **Samples**: Lightweight sample STLs are in `examples/stl/`

See [assets/README.md](assets/README.md) for detailed instructions.

## Development

For development, install in editable mode with development dependencies:

```bash
pip install -e .\[dev\]
```

