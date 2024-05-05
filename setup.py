#!/usr/bin/env python

"""setup.py: Controls the setup process using setuptools."""

import re

from setuptools import setup

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('uppyyl_observation_matcher_experiments/version.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name="uppyyl_observation_matcher_experiments",
    packages=["uppyyl_observation_matcher_experiments"],
    entry_points={
        "console_scripts": [
            'uppyyl_observation_matcher_experiments=uppyyl_observation_matcher_experiments.__main__:main',
            'uppyyl-observation-matcher-experiments=uppyyl_observation_matcher_experiments.__main__:main',
        ]
    },
    version=version,
    description="Experiments for Uppaal observation matching including a CLI tool.",
    long_description=long_description,
    author="Sascha Lehmann",
    author_email="s.lehmann@tuhh.de",
    url="",
    install_requires=[
        'uppyyl_observation_matcher',
        'matplotlib==3.5.1',
        'numpy==1.22.3',
        'pytest==7.1.2',
        'pytest-subtests==0.8.0',
        'colorama==0.4.4'
    ],
)
