from setuptools import setup

with open("src/czml3/version.txt") as f:
    version = f.read()

setup(version=version, package_data={"": ["czml3/version.txt"]})
