#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="apex-vdr-swarm",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vdr-swarm=apex_vdr_swarm.cli:main",
            "vdr-top=apex_vdr_swarm.cli:main",
        ],
    },
)
