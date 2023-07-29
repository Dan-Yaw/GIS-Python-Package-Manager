#!/usr/bin/env python
"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = []

test_requirements = []

setup(
    author="Daniel Yaw",
    author_email="danielyawjr@outlook.com",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="ArcGIS Online or Portal as a Python package manager!",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords="gis-python-package-manager",
    name="gis-python-package-manager",
    packages=find_packages(
        include=[
            "gis-python-package-manager",
            "gis-python-package-manager.*",
        ]
    ),
    package_dir={"": "src"},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/DanYawGISP/gismigrationtoolkit",
    version="0.1.1",
    zip_safe=False,
    entry_points={"console_scripts": ["gpip  = gis-python-package-manager:gpip:main"]},
)
