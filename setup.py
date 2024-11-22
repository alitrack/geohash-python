from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geohash-python",
    version="0.8.5",
    author="Steven Lee",
    author_email="alitrack.com@gmail.com",  # Add your email if you want
    description="A Python implementation of the Geohash algorithm compatible with python-geohash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alitrack/geohash-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[],
    test_suite="test",
    keywords=["geohash", "geo", "spatial", "location", "uint64", "gis"],
    project_urls={
        "Bug Tracker": "https://github.com/alitrack/geohash-python/issues",
        "Documentation": "https://github.com/alitrack/geohash-python",
        "Source Code": "https://github.com/alitrack/geohash-python",
    },
)
