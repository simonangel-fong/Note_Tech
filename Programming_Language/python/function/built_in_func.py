from functools import reduce
print("\n--------abs()--------\n")
# returns the absolute value of the specified number.
print(abs(-7.25))   # 7.25
print(abs(-10/4))   # 2.5
print(abs(3+5j))    # 5.830951894845301


print("\n--------round()--------\n")
# returns a floating point number that is a rounded version of the specified number, with the specified number of decimals.
# The default number of decimals is 0, meaning that the function will return the nearest integer.
# Parameter Description
# number    Required. The number to be rounded
# digits    Optional. The number of decimals to use when rounding the number. Default is 0
print(round(5.76443))       # 6
print(round(5.76443, 2))    # 5.76
print(round(5.76543, 2))    # 5.77


print("\n--------id()--------\n")
# returns a unique id for the specified object.
# All objects in Python has its own unique id.
# The id is assigned to the object when it is created.
# The id is the object's memory address, and will be different for each time you run the program. (except for some object that has a constant unique id, like integers from -5 to 256)
# Parameter Description
# object	Any object, String, Number, List, Class etc.
xStr = 'John'
print(id(xStr))             # 1624723905520
print(id("John"))           # 1624723905520

xInt = 5
print(id(xInt))             # 2109231557040
print(id(5))                # 2109231557040

xList = [1, 2, 3]
yList = xList
zList = xList.copy()
print(id([1, 2, 3]))        # 2591787877184
print(id(xList))            # 2591785232576
print(id(yList))            # 2591785232576
print(id(zList))            # 2591784915072


print("\n--------sorted()--------\n")
#  returns a sorted list of the specified iterable object.
# can specify ascending or descending order.
#   Strings are sorted alphabetically, and numbers are sorted numerically.
#   cannot sort a list that contains BOTH string values AND numeric values.
# Parameter	Description
# iterable	Required. The sequence to sort, list, dictionary, tuple etc.
# key	    Optional. A Function to execute to decide the order. Default is None
# reverse	Optional. A Boolean. False will sort ascending, True will sort descending. Default is False
xList = ("b", "g", "a", "d", "f", "c", "h", "e")
print(sorted(xList))                # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(sorted(xList, reverse=True))  # ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
# ('b', 'g', 'a', 'd', 'f', 'c', 'h', 'e'), the original iterable item is not changed.
print(xList)

xList = (1, 11, 2)
print(sorted(xList))        # [1, 2, 11]
print(xList)                # (1, 11, 2)


print("\n--------range()--------\n")
# returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number.
# Parameter	Description
# start	    Optional. An integer number specifying at which position to start. Default is 0
# stop	    Required. An integer number specifying at which position to stop (not included).
# step	    Optional. An integer number specifying the incrementation. Default is 1

print("\n--------range(): stop--------")
[print(x) for x in range(4)]
# 0
# 1
# 2
# 3

print("\n--------range(): start, stop--------")
[print(x) for x in range(2, 4)]
# 2
# 3

print("\n--------range(): start, stop, step--------")
[print(x) for x in range(3, 10, 3)]
# 3
# 6
# 9


print("\n--------enumerate()--------\n")
# takes a collection (e.g. a tuple) and returns it as an enumerate object.
# adds a counter as the key of the enumerate object.
# Parameter	Description
# iterable	An iterable object
# start	    A Number. Defining the start number of the enumerate object. Default 0

xEum = enumerate(('apple', 'banana', 'cherry'))
[print(index, item) for index, item in xEum]
# 0 apple
# 1 banana
# 2 cherry


print("\n--------map()--------\n")
# executes a specified function for each item in an iterable. The item is sent to the function as a parameter.
# map(function, iterables)
# Parameter	Description
# function	Required. The function to execute for each item
# iterable	Required. A sequence, collection or an iterator object. You can send as many iterables as you like, just make sure the function has one parameter for each iterable.


def xFunc(n):
    return len(n)


xMap = map(xFunc, ('apple', 'banana', 'cherry'))
print(xMap)            # <map object at 0x0000025F654055B0>
print(type(xMap))      # <class 'map'>
print(list(xMap))      # [5, 6, 6]
print([len(item) for item in ('apple', 'banana', 'cherry')])

print(list(map(lambda x: len(x), ('apple', 'banana', 'cherry'))))  # [5, 6, 6]

print(list(map(lambda x, y: x+'-'+y, ('apple', 'banana',
      'cherry'), ('orange', 'lemon', 'pineapple'))))
# ['apple-orange', 'banana-lemon', 'cherry-pineapple']


print("\n--------filter()--------\n")
# returns an iterator where the items are filtered through a function to test if the item is accepted or not.
# filter(function, iterable)
# Parameter	Description
# function	A Function to be run for each item in the iterable
# iterable	The iterable to be filtered


def xFunc(x):
    if x < 18:
        return False
    else:
        return True


xFilter = filter(xFunc, [5, 12, 17, 18, 24, 32])
print(xFilter)              # <filter object at 0x000002C1D0BE6E50>
print(type(xFilter))        # <class 'filter'>
print(list(xFilter))        # [18, 24, 32]


# [18, 24, 32]
print(list(filter(lambda x: x >= 18, [5, 12, 17, 18, 24, 32])))
print([item for item in [5, 12, 17, 18, 24, 32] if item >= 18])     # [18, 24, 32]


print("\n--------reduce()--------\n")
# need to import functools module
# Apply function of two arguments cumulatively to the items of iterable, from left to right, so as to reduce the iterable to a single value.
# reduce(function, iterable[, initializer]

print(reduce(lambda acc, item: acc+item, [5, 12, 17, 18, 24, 32]))       # 108
