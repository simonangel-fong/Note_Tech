import ctypes


class dynamic_array(object):
    '''
    DYNAMIC ARRAY CLASS (Similar to Python List)
    '''

    def __init__(self):
        self.size = 0       # Length of external array
        self.capacity = 1   # Length of internal array
        self.Arr = self._create_array(self.capacity)

    def _create_array(self, arr_capacity):
        """
        Returns a new array with arr_capacity capacity
        """
        return (arr_capacity * ctypes.py_object)()

    def __len__(self):
        """
        Return actual number of elements sorted in array
        """
        return self.size

    def _resize(self, new_cap):
        """
        Resize internal array to capacity new_cap
        """
        new_Arr = self._create_array(new_cap)  # New bigger array

        for i in range(self.size):     # loop all actual elements
            new_Arr[i] = self.Arr[i]

        self.Arr = new_Arr          # Call A the new bigger array
        self.capacity = new_cap     # Reset the capacity

    def __getitem__(self, index):
        """
        Return element at index
        """
        if not 0 <= index < self.size:
            return IndexError("Index is out of bounds!")
        return self.Arr[index]  # Retrieve from array at index k

    def append(self, element):
        """
        Add element to end of the array
        """
        if self.size == self.capacity:
            # Double capacity if not enough room
            self._resize(2*self.capacity)

        self.Arr[self.size] = element       # Set self.n index to element
        self.size += 1


print("\n--------Demo--------\n")

da = dynamic_array()

da.append(1)
da.append('two')
da.append({3})
da.append([4])
da.append({"key": 5})


[print(da[x]) for x in range(len(da))]
# 1
# two
# {3}
# [4]
# {'key': 5}
