import setuptools
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kobrakhan",
    version="0.0.1",
    author="Adam Bard",
    author_email="kobrakhan@adambard.com",
    description="Kobra Khan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adambard/kobra-khan",
    packages=setuptools.find_packages(include=['kobrakhan']),
    ext_modules=cythonize("kobrakhan/heuristics/*.pyx"),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
