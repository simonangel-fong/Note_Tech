# DSA - Hash Table

[Back](../index.md)

- [DSA - Hash Table](#dsa---hash-table)
  - [Hash Table](#hash-table)
  - [Time Complexity](#time-complexity)
  - [Hash Function](#hash-function)
  - [Collision Resolution](#collision-resolution)
  - [Implement Hash Table](#implement-hash-table)
    - [Constructor](#constructor)
    - [Set\_value(): `O(1)`](#set_value-o1)
    - [Get\_value(): `O(1)`](#get_value-o1)
    - [Keys(): `O(1)`](#keys-o1)
  - [Implement Hash Table in Python](#implement-hash-table-in-python)
  - [Classic: Check if common item exists](#classic-check-if-common-item-exists)

---

## Hash Table

- `Hashing`

  - the process of using a mathematical function to **convert input data into a fixed-length output**.
  - can **reduce the size** of the store value.
  - an one-way process and is deterministic.

- `Hash table`

  - a data structure that can be searched in `O(1)` time.

- `Slots`

  - the position of the hash table that can hold an item and are named by an integer value starting at 0.
  - Initially, the hash table contains no items so every slot is **empty**.

- Characteristics of Hash
  - One way
  - Deterministic

---

## Time Complexity

- By assumption, items in hash table are usually evenly distributed. Collision rarely happens.
- So, the big O of setting and looking up value is `O(0)`.

---

## Hash Function

- `Hashing function`

  - A function **maps between an item and the slot** where that item belongs in the hash table
  - takes any item in the collection and **return an integer in the range of slot names**, between 0 and m-1. 返回 slot 名
  - accepts arbitrary size value and maps it to a **fixed-size data structure**.

- `Perfect hash function`

  - A hash function that maps each item into a unique slot

- **Non-integer** elements

  - strings as a sequence of **ordinal values**.

        h(item)=sum(ordinal values)%len(slot_arr)

- **Remainder Method**

  - remainder hash function then is:

        h(item)=item%len(slot_arr)

- **Folding Method**

  - dividing the item into equal-size pieces (the last piece may not be of equal size).
  - These pieces are then added together to give the resulting hash value.

        h(item)=sum(group_digits)%len(slot_arr)

- **Mid Square Method**
  - For the mid-square method we first square the item, and then extract some portion of the resulting digits.
  - For example, if the item were 44, we would first compute 442=1,936.
  - By extracting the middle two digits, 93, and performing the remainder step, we get 93%11 =5

---

## Collision Resolution

- `collision`

  - one slot has two items

- `load factor`

  - represents the load that is there on our map.
  - `numberofitems / tablesize`
  - needs to be kept low, so that **number of entries** at one index is less and so is the complexity almost constant, i.e., `O(1)`.需要越低越好, 减少同一 slot 重复出现可能,从而提高效率.

- `Open addressing`

  - a collision **resolution** process that tries to **find the next open slot or address** in the hash table.
  - We could start at the original hash value position and then **move in a sequential manner through the slots until we encounter the first slot that is empty.**

  - `rehashing`

    - the process to look for another slot after a collision.

  - `linear probing`

    - an open addressing technique by systematically visiting each slot one at a time. 逐个访问 slot

  - `quadratic probing`
    - to skip slots, thereby more evenly distributing the items that have caused collisions.
    - use a rehash function that increments the hash value by 1, 3, 5, 7, 9, and so on. If the first hash value is h, the successive values are h+1, h+4, h+9, h+16, and so on.
    - 跳过令到更加平均分布

- `Separate Chaining`

  - allow each **slot to hold a reference to a collection** (or chain) of items.
  - allows many items to exist at the same location in the hash table.
  - As more and more items hash to the same location, the difficulty of searching for the item in the collection increases.

---

## Implement Hash Table

### Constructor

```py
class HashTable:
    def __init__(self, size=7):
        self.data_map = [None]*size

    def __hash(self, key):
        my_hash = 0
        for letter in key:
            # ord(): return ascii number of each letter
            # 23 is a prime number; Here can be any prime number
            my_hash = (my_hash + ord(letter)*23) % len(self.data_map)
        return my_hash

    def print_table(self):
        for i, val in enumerate(self.data_map):
            print(i, ':', val)


my_hash_table = HashTable()

my_hash_table.print_table()
```

---

### Set_value(): `O(1)`

```py
def set_item(self, key, value):
    # compute the hash index
    index = self.__hash(key)
    # when the index is empty, then initiate with a list
    if self.data_map[index] is None:
        self.data_map[index] = []
    # if the index is empty, it has been fill with an empty list, then append key-value pair
    # if the index has been filled, append key-value pair to the existing list.
    self.data_map[index].append([key, value])
```

---

### Get_value(): `O(1)`

```py
def get_item(self, key):
    index = self.__hash(key)

    if self.data_map[index] is None:
        return None

    for item in self.data_map[index]:
        if item[0] == key:
            return item[1]

    return None
```

---

### Keys(): `O(1)`

```py
def keys(self):
    all_keys = []
    for i in range(len(self.data_map)):
        if self.data_map[i] is not None:
            for j in range(len(self.data_map[i])):
                all_keys.append(self.data_map[i][j][0])
    return all_keys
```

---

## Implement Hash Table in Python

- using a `list` with each element initialized to the special Python value `None`.

- The idea of a dictionary used as a hash table to get and retrieve items using **keys** is often referred to as a mapping. In our implementation we will have the following methods:

- **HashTable()** Create a new, empty map. It returns an empty map collection.
- **put(key,val)** Add a new key-value pair to the map. If the key is already in the map then replace the old value with the new value.
- **get(key)** Given a key, return the value stored in the map or None otherwise.
- **del** Delete the key-value pair from the map using a statement of the form del map[key].
- **len()** Return the number of key-value pairs stored
- **in** the map in Return True for a statement of the form **key in map**, if the given key is in the map, False otherwise.

- 思路:
  - 一个数组 slot, 用于记录 key; 一个数组 data, 用于存储 item
  - 使用相同的 index 关联
  - 在数学上, str 可以转化为数字, 所以 key 一定是数字
  - 使用 `hash function` 将 key 转化为 `hash code`, 根据 hash code 将 key 存入 相应的 index 的 slot; 将 item 存入相应 index 的 data.
  - 因为给定的 key 一定有相同的 hash code, 所以有确定的 index, 所以 key 和 item 通过确定 index 关联.
  - 冲突: 不同的 key 可能有相同 hash code
    - load factor, 衡量负载度
    - 方法 1: Open addressing 寻找下一个空 slot
      - rehashing, 寻找下一个空 slot 的方法
      - linear probing, 按顺序延申
      - quadratic probing, 按平方跳过延申
    - 方法 2: Chaining 相同 slot 存储多个, 可能会降低性能

```py
class hash_table(object):

    def __init__(self, size):
        self.size = size
        self.slot = [None] * self.size
        self.data = [None] * self.size

    def __getitem__(self, key):
        return self._get(key)

    def __setitem__(self, key, item):
        self._put(key, item)

    def _put(self, key, item):
        hash_code = self.hash_function(key)

        # if slot is empty
        if self.slot[hash_code] == None:
            self.slot[hash_code] = key
            self.data[hash_code] = item

        # when colision
        else:

            # open addressing, probe for next empty slot
            # loop until next slot is empty or the key exists
            while self.slot[hash_code] != None and self.slot[hash_code] != key:
                hash_code = self.rehash_function(hash_code)

            # when the key exists, overwrite data
            # self.slot[hash_code] == key
            if self.slot[hash_code] != None:
                self.data[hash_code] = item

            # when the slot is empty, store key and data
            # self.slot[hash_code] == None
            if self.slot[hash_code] != key:
                self.slot[hash_code] = key
                self.data[hash_code] = item

    def _get(self, key):
        start_code = hash_code = self.hash_function(key)
        # print(self.slot)
        # if slot is not empty but not match,  rehash
        # when colision
        if self.slot[hash_code] != None and self.slot[hash_code] != key:
            # rehash until next None, or key matches
            while self.slot[hash_code] != None and self.slot[hash_code] != key:
                hash_code = self.rehash_function(hash_code)

                # in case of slot full and not matches, when loop back to start, break
                if hash_code == start_code:
                    break

            # when next slot is None, or when key matches, return data
            # return might be None
            return self.data[hash_code]

        # when not colision
        # return might be None, or data
        else:
            return self.data[hash_code]

    def hash_function(self, key):
        # Remainder Method
        if isinstance(key, str):
            return sum([ord(ch) for ch in key]) % len(self.slot)
        return key % len(self.slot)

    def rehash_function(self, old_hash_code):
        return (old_hash_code+1) % len(self.slot)     # linear probing

```

---

## Classic: Check if common item exists

```py
# method using set(): python method
def item_in_common(list1, list2):
    s1 = set(list1)
    s2 = set(list2)

    return len(s1.intersection(s2)) > 0


# using for loop: O(n^2)
def item_in_common(list1, list2):
    for i in list1:
        for j in list2:
            if i == j:
                return True
    return False


# method using hash table: O(1)
def item_in_common(list1, list2):
    my_dict = {}
    for i in list1:
        my_dict[i] = True

    for j in list2:
        if j in my_dict:
            return True

    return False


list1 = [1,3,5]
list2 = [2,4,6]

print(item_in_common(list1, list2))
```

---

[TOP](#dsa---hash-table)
