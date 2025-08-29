# pyfusefilter

If you work with large sets—such as thousands or millions of URLs, user IDs, or other keys—and need to quickly check whether an element is present, these filters provide exceptional speed and minimal memory usage. They are ideal for applications where you want to efficiently exclude elements not in your set, with much lower overhead than traditional approaches like sets or even Bloom filters.


## Installation
`pip install pyfusefilter`


## API

[API Documentation](https://fastfilter.github.io/pyfusefilter/)

## Usage



The filters Xor8 and Fuse8 use slightly over a byte of memory per entry, with a false positive rate of about 0.39%. The filters Xor16 and Fuse16 use slightly over two bytes of memory per entry, with a false positive rate of about 0.0015%. For large sets, Fuse8 and Fuse16 filters use slightly more memory and they can be built
faster.



```py
>>> from pyfusefilter import Xor8, Xor16, Fuse8, Fuse16
>>> 
>>> #Supports unicode strings and heterogeneous types
>>> test_str = ["あ","अ", 51, 0.0, 12.3]
>>> filter = Xor8(test_str)	
True
>>> filter.contains("अ")
True
>>> filter[51]  #You can use __getitem__ instead of contains
True
>>> filter["か"]
False
>>> filter.size_in_bytes()
60
```


The `size_in_bytes()` function gives the memory usage of the filter itself. It does not count
the Python overhead which adds a few bytes to the actual memory usage.

You can serialize a filter with the `serialize()` method which returns a buffer, and you can recover the filter with the `deserialize(buffer)` method, which returns a filter:

```py
> f = open('/tmp/output', 'wb')
> f.write(filter.serialize())
> f.close()
> recoverfilter = Xor8.deserialize(open('/tmp/output', 'rb').read())
```

The serialization format is as concise as possible and will typically use a few bytes
less than `size_in_bytes()`.

## Measuring data usage

 The actual memory usage is slightly higher (there is a small constant overhead) due to
Python metadata.

```python
from pyfusefilter import Xor8, Fuse8

N = 100
while (N < 10000000):
    # filters can be initialized with an integer, the memory is allocated, but unused.
    # call 'populate' to fill them with data.
    filter = Xor8(len(data))
    fusefilter = Fuse8(len(data))
    print(N, filter.size_in_bytes()/N, fusefilter.size_in_bytes()/N)
    N *= 10

```


## False-positive rate
For more accuracy(less false positives) use larger but more accurate Xor16 for Fuse16.

For large sets (contain millions of keys), Fuse8/Fuse16 filters are faster and smaller than Xor8/Xor16.

```py
>>> filter = Xor8(1000000)
>>> filter.size_in_bytes()
1230054
>>> filter = Fuse8(1000000)
>>> filter.size_in_bytes()
1130536
```

### From Source

Assuming that your Python interpreter is called `python`.

```bash
# Clone the repository with submodules
git clone --recurse-submodules https://github.com/glitzflitz/pyfusefilter
cd pyfusefilter

# If you forgot --recurse-submodules, initialize submodules now
git submodule update --init --recursive

# Create and activate virtual environment
python -m venv pyfuseenv
source pyfuseenv/bin/activate  # On Windows: pyfuseenv\Scripts\activate

# Install build dependencies
python -m pip install setuptools wheel cffi xxhash

# Build the CFFI extension
python setup.py build_ext

# Install the package
python setup.py install

# Optional: Run tests to verify installation
python -m pip install pytest
python -m pytest tests/ -v

# Generate documentation
python -m pip install pdoc
python -m pdoc pyfusefilter --output-dir docs
```

**Notes:**
- The build process compiles C code using your system's C compiler
- On macOS, you may need to install Xcode command line tools: `xcode-select --install`
- On Linux, install development headers: `apt-get install python3-dev` (Ubuntu/Debian) or `yum install python3-devel` (CentOS/RHEL)



### Local Documentation

To generate documentation locally:

```bash
# Install pdoc
pip install pdoc

# Generate documentation
pdoc pyfusefilter --output-dir docs

# View locally
python -m http.server 8000
# Open http://localhost:8000/docs/
```

### References

- [Binary Fuse Filters: Fast and Smaller Than Xor Filters](http://arxiv.org/abs/2201.01174), Journal of Experimental Algorithmics 27, 2022.
- [Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters](https://arxiv.org/abs/1912.08258), Journal of Experimental Algorithmics 25 (1), 2020


## Links
* [C Implementation](https://github.com/FastFilter/xor_singleheader)
* [Go Implementation](https://github.com/FastFilter/xorfilter)
* [Erlang bindings](https://github.com/mpope9/exor_filter)
* Rust Implementation: [1](https://github.com/bnclabs/xorfilter) and [2](https://github.com/codri/xorfilter-rs)
* [C++ Implementation](https://github.com/FastFilter/fastfilter_cpp)
* [Java Implementation](https://github.com/FastFilter/fastfilter_java)
