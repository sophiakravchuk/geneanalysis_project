import ctypes


class Array:
    """Creates an array with size elements."""
    def __init__(self, size):
        """
        Create the array structure using the ctypes module.
        Initialize each element.
        """
        if size < 0:
            raise ValueError("Array size must be > 0")
        self._size = size
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        self.clear(None)

    def __len__(self):
        """Returns the size of the array."""
        return self._size

    def __getitem__(self, index):
        """
        Gets the contents of the index element.
        """
        if not index >= 0 and index < len(self):
            raise IndexError("Array subscript out of range")
        return self._elements[index]

    def __setitem__(self, index, value):
        """
        Puts the value in the array element at index position.
        """
        if not index >= 0 and index < len(self):
            raise IndexError("Array subscript out of range")
        self._elements[index] = value

    def clear(self, value):
        """Clears the array by setting each element to the given value."""
        for i in range(len(self)):
            self._elements[i] = value

    def __str__(self):
        s = "["
        for i in self._elements:
            s += str(i) + ","
        s = s[:-1]
        s += "]"
        return s


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""
    INITIAL_CAPACITY = 1

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # count actual elements
        self._A = self._make_array(DynamicArray.INITIAL_CAPACITY)  # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]  # retrieve from array

    def append(self, obj):
        """Add object to end of the array."""
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):  # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array

    def _make_array(self, c):  # nonpublic utitity
        """Return new array with capacity c."""
        return Array(c)  # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value( or  raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item

                return  # exit immediately
        raise ValueError("value not found")  # only reached if no match

    def __str__(self):
        res = []
        for i in range(self._n):
            res.append(str(self._A[i]))
        return ", ".join(res)

    def pop(self):
        last = self._A[self._n - 1]
        self._n -= 1
        return last

    def clear(self, value=None):
        """Clears the array by setting each element to the given value."""
        for i in range(len(self)):
            self._A[i] = value
        self._n = 0
