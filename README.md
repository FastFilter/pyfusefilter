# pyfusefilter

Python bindings for [C](https://github.com/FastFilter/xor_singleheader) implementation of [Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters](https://arxiv.org/abs/1912.08258)
and of [Binary Fuse Filters: Fast and Smaller Than Xor Filters](https://arxiv.org/abs/2201.01174).



## Installation
`pip install pyfusefilter`
### From Source
```
git clone --recurse-submodules https://github.com/glitzflitz/pyfusefilter
cd pyfusefilter
python setup.py build_ext
python setup.py install
```
## Usage

The filters Xor8 and Fuse8 use slightly over a byte of memory per entry, with a false positive rate of about 0.39%.
The filters Xor16 and Fuse16 use slightly over two bytes of memory per entry, with a false positive rate of about 0.0015%.



```py
>>> from pyfusefilter import Xor8, Xor16, Fuse8, Fuse16
>>> 
>>> #Supports unicode strings and heterogeneous types
>>> test_str = ["あ","अ", 51, 0.0, 12.3]
>>> filter = Xor8(len(test_str))	#or Xor16(size)
>>> filter.populate(test_str)
True
>>> filter.contains("अ")
True
>>> filter[51]  #You can use __getitem__ instead of contains
True
>>> filter["か"]
False
>>> filter.contains(150)
False
>>> filter.size_in_bytes()
60
```

You can serialize a filter with the `serialize()` method which returns a buffer, and you can recover the filter with the `deserialize(buffer)` method, which returns a filter:

```py
> f = open('/tmp/output', 'wb')
> f.write(filter.serialize())
> f.close()
> recoverfilter = Xor8.deserialize(open('/tmp/output', 'rb').read())
```

## Measuring data usage

The `size_in_bytes()` function gives the memory usage of the filter itself. The actual memory usage is slightly higher (there is a small constant overhead) due to
Python metadata.

```python
    from pyfusefilter import Xor8, Fuse8

    N = 100
    while (N < 10000000):
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



## References

- [Binary Fuse Filters: Fast and Smaller Than Xor Filters](http://arxiv.org/abs/2201.01174), Journal of Experimental Algorithmics 27, 2022.
- [Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters](https://arxiv.org/abs/1912.08258), Journal of Experimental Algorithmics 25 (1), 2020


## Links
* [C Implementation](https://github.com/FastFilter/xor_singleheader)
* [Go Implementation](https://github.com/FastFilter/xorfilter)
* [Erlang bindings](https://github.com/mpope9/exor_filter)
* Rust Implementation: [1](https://github.com/bnclabs/xorfilter) and [2](https://github.com/codri/xorfilter-rs)
* [C++ Implementation](https://github.com/FastFilter/fastfilter_cpp)
* [Java Implementation](https://github.com/FastFilter/fastfilter_java)
