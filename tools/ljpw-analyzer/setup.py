from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ljpw-analyzer",
    version="0.1.0",
    author="LJPW Framework Contributors",
    description="Open-source tool for analyzing systems using the LJPW framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BruinGrowly/Universal-System-Physics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    entry_points={
        "console_scripts": [
            "ljpw-analyzer=ljpw_analyzer:main",
        ],
    },
)
