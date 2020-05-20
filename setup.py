"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='panda3d-logos',
    version='0.1',
    description='Logos for Panda3D',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/janEntikan/panda3d-logos',
    author='janEntikan',
    keywords='panda3d',
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
    python_requires='>=3.4, <4',
    install_requires=['panda3d'],
    entry_points={
        'console_scripts': [
            'panda3dsplash=panda3dsplash:main',
        ],
    },
)
