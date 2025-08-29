from setuptools import setup, Extension, find_packages
import os

setup(
    name="pyfusefilter",
    version="1.0.0",
    description="Python bindings for C implementation of xorfilter",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Amey Narkhede",
    author_email="ameynarkhede02@gmail.com",
    url="https://github.com/glitzflitz/pyfusefilter",
    license="Apache 2.0",
    python_requires=">=3.0",
    packages=find_packages(),
    ext_package="pyfusefilter",
    install_requires=["cffi","xxhash"],
    cffi_modules=["pyfusefilter/ffibuild.py:ffi"],
)

