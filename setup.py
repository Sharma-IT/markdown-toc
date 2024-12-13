from setuptools import setup, find_packages

setup(
    name="markdown-toc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "markdown-toc=src.cli:main",
        ],
    },
    author="Shubham Sharma",
    author_email="shubhamsharma.emails@gmail.com",
    description="A tool for generating Table of Contents in markdown files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sharma-IT/markdown-toc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
