from ._xorfilter import lib, ffi
from ctypes import c_ulonglong
import xxhash
import struct

def hash(item):
    return xxhash.xxh64(str(item)).intdigest()

class Xor8:
    """
    Xor8 is a probabilistic data structure that allows for fast set membership queries.
    It may return false positives but never false negatives. It uses slightly more than
    a byte of memory per key. Its false positive rate is roughly 0.39%.
    For large sets, a Fuse8 filter is more efficient than a Xor8 filter.
    """
    def __init__(self, size_or_data):
        """
        Initialize the Xor8 filter.
        If an integer is provided, allocate a filter of that size. You must then use 'populate' to add data.
        If an iterable is provided, populate the filter with the data.
        """
        self.__filter = ffi.new("xor8_t *")
        if isinstance(size_or_data, int):
            status = lib.xor8_allocate(size_or_data, self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
        else:
            data = list(size_or_data)
            status = lib.xor8_allocate(len(data), self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
            else:
                data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
                lib.xor8_buffered_populate(data, len(data), self.__filter)

    def __repr__(self):
        return "Xor8 object with size(in bytes):{}".format(self.size_in_bytes())

    def __getitem__(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        return self.contains(item)

    def __del__(self):
        lib.xor8_free(self.__filter)

    def populate(self, data: list):
        """
        Set the data of the filter. You may use this method to add data after
        allocating the filter with an integer size. The sizes should match.
        You can reuse a filter with new data (i.e., call populate several times)
        as long as the size remains a constant.
        """
        data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
        return lib.xor8_buffered_populate(data, len(data), self.__filter)

    def contains(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        item = c_ulonglong((hash(item))).value
        return lib.xor8_contain(item, self.__filter)

    def size_in_bytes(self):
        """
        Return the size of the filter in bytes, not counting Python overhead.
        This value might be slightly larger than the serialized size.
        """
        return lib.xor8_size_in_bytes(self.__filter)
    
    def serialize(self):
        """
        Serialize the filter to a bytes object.
        """
        buffer = ffi.new("char[]", lib.xor8_serialization_bytes(self.__filter))
        lib.xor8_serialize(self.__filter, buffer)
        return ffi.buffer(buffer)

    @staticmethod
    def deserialize(buffer):
        """
        Deserialize a bytes object to a Xor8 filter.
        """
        self = object.__new__(Xor8)
        self.__filter = ffi.new("xor8_t *")
        lib.xor8_deserialize(self.__filter, ffi.from_buffer(buffer))
        return self


class Xor16:
    """
    Xor16 is a probabilistic data structure that allows for fast set membership queries.
    It may return false positives but never false negatives. It uses about two bytes of memory per key.
    Its false positive rate is roughly 0.0015%.
    For large sets, a Fuse16 filter is more efficient than a Xor16 filter.
    """
    def __init__(self, size_or_data):
        """
        Initialize the Xor16 filter.
        If an integer is provided, allocate a filter of that size. You must then use 'populate' to add data.
        If an iterable is provided, populate the filter with the data.
        """
        self.__filter = ffi.new("xor16_t *")
        if isinstance(size_or_data, int):
            status = lib.xor16_allocate(size_or_data, self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
        else:
            data = list(size_or_data)
            status = lib.xor16_allocate(len(data), self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
            else:
                data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
                lib.xor16_buffered_populate(data, len(data), self.__filter)

    def __repr__(self):
        """
        Return a string representation of the Xor16 filter, including its size in bytes.
        """
        return "Xor16 object with size(in bytes):{}".format(self.size_in_bytes())

    def __getitem__(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        return self.contains(item)

    def __del__(self):
        """
        Free the memory allocated for the Xor16 filter.
        """
        lib.xor16_free(self.__filter)

    def populate(self, data):
        """
        Set the data of the filter. You may use this method to add data after
        allocating the filter with an integer size. The sizes should match.
        You can reuse a filter with new data (i.e., call populate several times)
        as long as the size remains a constant.
        """
        data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
        return lib.xor16_buffered_populate(data, len(data), self.__filter)

    def contains(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        item = c_ulonglong((hash(item))).value
        return lib.xor16_contain(item, self.__filter)

    def size_in_bytes(self):
        """
        Return the size of the filter in bytes, not counting Python overhead.
        This value might be slightly larger than the serialized size.
        """
        return lib.xor16_size_in_bytes(self.__filter)

    def serialize(self):
        """
        Serialize the filter to a bytes object.
        """
        buffer = ffi.new("char[]", lib.xor16_serialization_bytes(self.__filter))
        lib.xor16_serialize(self.__filter, buffer)
        return ffi.buffer(buffer)

    @staticmethod
    def deserialize(buffer):
        """
        Deserialize a bytes object to a Xor16 filter.
        """
        self = object.__new__(Xor16)
        self.__filter = ffi.new("xor16_t *")
        lib.xor16_deserialize(self.__filter, ffi.from_buffer(buffer))
        return self

class Fuse8:
    """
    Fuse8 is a probabilistic data structure for fast set membership queries.
    It offers a balance between speed and memory usage, with a false positive rate of about  0.39%.
    It uses about one byte of memory per key.
    For large sets, a Fuse8 filter is more efficient than a Xor8 filter.
    """
    def __init__(self, size_or_data):
        """
        Initialize the Fuse8 filter.
        If an integer is provided, allocate a filter of that size. You must then use 'populate' to add data.
        If an iterable is provided, populate the filter with the data.
        """
        self.__filter = ffi.new("binary_fuse8_t *")
        if isinstance(size_or_data, int):
            status = lib.binary_fuse8_allocate(size_or_data, self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
        else:
            data = list(size_or_data)
            status = lib.binary_fuse8_allocate(len(data), self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
            else:
                data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
                lib.binary_fuse8_populate(data, len(data), self.__filter)

    def __repr__(self):
        """
        Return a string representation of the Fuse8 filter, including its size in bytes.
        """
        return "Fuse8 object with size(in bytes):{}".format(self.size_in_bytes())

    def __getitem__(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        return self.contains(item)

    def __del__(self):
        """
        Free the memory allocated for the Fuse8 filter.
        """
        lib.binary_fuse8_free(self.__filter)

    def populate(self, data: list):
        """
        Set the data of the filter. You may use this method to add data after
        allocating the filter with an integer size. The sizes should match.
        You can reuse a filter with new data (i.e., call populate several times)
        as long as the size remains a constant.
        """
        data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
        return lib.binary_fuse8_populate(data, len(data), self.__filter)

    def contains(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        item = c_ulonglong((hash(item))).value
        return lib.binary_fuse8_contain(item, self.__filter)

    def size_in_bytes(self):
        """
        Return the size of the filter in bytes, not counting Python overhead.
        This value might be slightly larger than the serialized size.
        """
        return lib.binary_fuse8_size_in_bytes(self.__filter)

    def serialize(self):
        """
        Serialize the filter to a bytes object.
        """
        buffer = ffi.new("char[]", lib.binary_fuse8_serialization_bytes(self.__filter))
        lib.binary_fuse8_serialize(self.__filter, buffer)
        return ffi.buffer(buffer)

    @staticmethod
    def deserialize(buffer):
        """
        Deserialize a bytes object to a Fuse8 filter.
        """
        self = object.__new__(Fuse8)
        self.__filter = ffi.new("binary_fuse8_t *")
        lib.binary_fuse8_deserialize(self.__filter, ffi.from_buffer(buffer))
        return self

class Fuse16:
    """
    Fuse16 is a probabilistic data structure that allows for fast set membership queries.
    It may return false positives but never false negatives. It uses about two bytes of memory per key.
    Its false positive rate is roughly 0.0015%.
    For large sets, a Fuse16 filter is more efficient than a Xor16 filter.
    """
    def __init__(self, size_or_data):
        """
        Initialize the Fuse16 filter.
        If an integer is provided, allocate a filter of that size. You must then use 'populate' to add data.
        If an iterable is provided, populate the filter with the data.
        """
        self.__filter = ffi.new("binary_fuse16_t *")
        if isinstance(size_or_data, int):
            status = lib.binary_fuse16_allocate(size_or_data, self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
        else:
            data = list(size_or_data)
            status = lib.binary_fuse16_allocate(len(data), self.__filter)
            if not status:
                raise MemoryError("Unable to allocate memory for filter")
            else:
                data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
                lib.binary_fuse16_populate(data, len(data), self.__filter)

    def __repr__(self):
        """
        Return a string representation of the Fuse16 filter, including its size in bytes.
        """
        return "Fuse16 object with size(in bytes):{}".format(self.size_in_bytes())

    def __getitem__(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        return self.contains(item)

    def __del__(self):
        """
        Free the memory allocated for the Fuse16 filter.
        """
        lib.binary_fuse16_free(self.__filter)

    def populate(self, data: list):
        """
        Set the data of the filter. You may use this method to add data after
        allocating the filter with an integer size. The sizes should match.
        You can reuse a filter with new data (i.e., call populate several times)
        as long as the size remains a constant.
        """
        data = list(map(lambda x: c_ulonglong((hash(x))).value, data))
        return lib.binary_fuse16_populate(data, len(data), self.__filter)

    def contains(self, item):
        """
        Check if the item is in the filter. With a small probability, the filter
        may return true for an item not in the set (false positive). There is
        no false negative: if the filter returns false, the item is definitely not in the set.
        """
        item = c_ulonglong((hash(item))).value
        return lib.binary_fuse16_contain(item, self.__filter)

    def size_in_bytes(self):
        """
        Return the size of the filter in bytes, not counting Python overhead.
        This value might be slightly larger than the serialized size.
        """
        return lib.binary_fuse16_size_in_bytes(self.__filter)

    def serialize(self):
        """
        Serialize the filter to a bytes object.
        """
        buffer = ffi.new("char[]", lib.binary_fuse16_serialization_bytes(self.__filter))
        lib.binary_fuse16_serialize(self.__filter, buffer)
        return ffi.buffer(buffer)

    @staticmethod
    def deserialize(buffer):
        """
        Deserialize a bytes object to a Fuse16 filter.
        """
        self = object.__new__(Fuse16)
        self.__filter = ffi.new("binary_fuse16_t *")
        lib.binary_fuse16_deserialize(self.__filter, ffi.from_buffer(buffer))
        return self