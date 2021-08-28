from setuptools import find_packages
from setuptools import setup
from pathlib import Path

setup(
    name="DndEncounterSimulator",
    install_requires=Path("requirements.txt").read_text().splitlines(),
    packages=find_packages(),
    include_package_data=True,
)