#!/usr/bin/env python3
"""Example showing how to use environment variables loaded by solx package.
"""

import os

import solx  # This will automatically load the .env file


def main():
    # Environment variables are now available throughout the application
    output_dir = os.getenv("OUTPUT_STR_DIR_PATH", "default_output")
    print(f"Output directory from .env: {output_dir}")

    # Create a simple cube and save it
    cube = solx.Cube(size=[10, 10, 10])

    # Use the environment variable for output path
    print(f"Using environment variable: OUTPUT_STR_DIR_PATH = {output_dir}")


if __name__ == "__main__":
    main()
