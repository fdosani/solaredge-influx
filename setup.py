from setuptools import setup, find_packages
import os

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURR_DIR, "README.md"), encoding="utf-8") as file_open:
    LONG_DESCRIPTION = file_open.read()

with open("requirements.txt", "r") as requirements_file:
    raw_requirements = requirements_file.read().strip().split("\n")

INSTALL_REQUIRES = [
    line for line in raw_requirements if not (line.startswith("#") or line == "")
]


exec(open("seinflux/_version.py").read())

setup(
    name="seinflux",
    version=__version__,
    description="Monitoring your SolarEdge Inverter",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/fdosani/seinflux",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require={"dev": ["black", "pytest"]},
    py_modules=["seinflux"],
    entry_points="""
            [console_scripts]
            seinflux=seinflux.seinflux:cli
        """,
)
