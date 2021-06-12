"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='panda3d-logos',
    version='0.12',
    description='The Panda3D logo in various formats, a 3d animated splash screen and code to show it off.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thecheapestpixels/panda3d-logos',
    author='thecheapestpixels',
    keywords='panda3d',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['panda3d'],
    entry_points={
        'console_scripts': [
            'panda3dsplash=panda3d_logos.panda3dsplash:main',
        ],
    },
)
