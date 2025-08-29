from setuptools import setup, Extension, find_packages
import os

setup(
    name="pyfusefilter",
    version="1.1.2",
    description="Python bindings for C implementation of xorfilter",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Amey Narkhede & Daniel Lemire",
    author_email="daniel@lemire.me",
    url="https://github.com/FastFilter/pyfusefilter",
    # license handled in pyproject.toml
    python_requires=">=3.0",
    packages=find_packages(),
    ext_package="pyfusefilter",
    # install_requires handled in pyproject.toml
    cffi_modules=["pyfusefilter/ffibuild.py:ffi"],
)

