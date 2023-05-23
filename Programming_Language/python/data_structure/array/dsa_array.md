# DSA - Array

[Back](../../index.md)

- [DSA - Array](#dsa---array)
  - [List](#list)
  - [Implement Dynamic Array in Python](#implement-dynamic-array-in-python)
  - [Problem: Array](#problem-array)
    - [Anagram Check](#anagram-check)
    - [Pair Sum](#pair-sum)
    - [Find the Missing Element](#find-the-missing-element)
    - [Largest Continuous Sum](#largest-continuous-sum)
    - [Sentence Reversal](#sentence-reversal)
    - [String Compression](#string-compression)
    - [Unique Characters in String](#unique-characters-in-string)

---

## List

- **Array Based Sequences**

  - the "sequence" type object classes available in Python are mainly the **list**,**tuple**, and **string** objects.
  - The main commonaility between these object types is **the ability to index to access** individual elements in the sequence.

- In Python `lists` **act as dynamic arrays** and support a number of common operations through **methods** called on them.
- The two most common operations performed on a list are **indexing** and **assigning** to an index position.

  - These operations are both designed to be run in constant time, `O(1)`.

- In Python, the most effective **method to create** a list is the built-in `list()` function.

<table>
        <tr>
            <th>Operation </th>
            <th>Big-O Efficiency</th>
        </tr>
    <tr>
        <td>index []</td>
        <td>O(1)</td>
    </tr>
    <tr>
        <td>index assignment</td>
        <td>O(1)</td>
    </tr>
    <tr>
        <td>append</td>
        <td>O(1)</td>
    </tr>
    <tr>
        <td>pop()</td>
        <td>O(1)</td>
    </tr>
    <tr>
        <td>pop(i)</td>
        <td>O(n)</td>
    </tr>
    <tr >
        <td>insert(i,item)</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>del operator</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>iteration</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>contains (in)</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>get slice [x:y]</td>
        <td>O(k)</td>
    </tr>
    <tr>
        <td>del slice</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>set slice</td>
        <td>O(n+k)</td>
    </tr>
    <tr>
        <td>reverse</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>concatenate</td>
        <td>O(k)</td>
    </tr>
    <tr>
        <td>sort</td>
        <td>O(n log n)</td>
    </tr>
    <tr>
        <td>multiply</td>
        <td>O(nk)</td>
    </tr>

</table>

---

## Implement Dynamic Array in Python

```py
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

```

---

## Problem: Array

### Anagram Check

Given two strings, check to see if they are anagrams. An anagram is when the two strings can be written using the exact same letters (so you can just rearrange the letters to get a different phrase or word).

- For example:
  - "public relations" is an anagram of "crap built on lies."
  - "clint eastwood" is an anagram of "old west action"

**Note: Ignore spaces and capitalization. So "d go" is an anagram of "God" and "dog" and "o d g".**

[Anagram Check problem](./problem_anagram_check.ipynb)

---

### Pair Sum

Given an integer array, output all the ** _unique_ ** pairs that sum up to a specific value **k**.

So the input:

    pair_sum([1,3,2,2],4)

would return **2** pairs:

     (1,3)
     (2,2)

**NOTE: FOR TESTING PURPOSES CHANGE YOUR FUNCTION SO IT OUTPUTS THE NUMBER OF PAIRS**

[Pair Sum problem](./problem_pair_sum.ipynb)

---

### Find the Missing Element

Consider an array of non-negative integers. A second array is formed by shuffling the elements of the first array and deleting a random element. Given these two arrays, find which element is missing in the second array.

Here is an example input, the first array is shuffled and the number 5 is removed to construct the second array.

Input:

    finder([1,2,3,4,5,6,7],[3,7,2,1,4,6])

Output:

    5 is the missing number

[Find the Missing Element problem](./problem_find_missing_element.ipynb)

---

### Largest Continuous Sum

Given an array of integers (positive and negative) find the largest continuous sum.

[Largest Continuous Sum problem](./problem_largest_continuous_sum.ipynb)

---

### Sentence Reversal

Given a string of words, reverse all the words. For example:

Given:

    'This is the best'

Return:

    'best the is This'

As part of this exercise you should remove all leading and trailing whitespace. So that inputs such as:

    '  space here'  and 'space here      '

both become:

    'here space'

[Sentence Reversal problem](./problem_sentence_reversal.ipynb)

---

### String Compression

Given a string in the form 'AAAABBBBCCCCCDDEEEE' compress it to become 'A4B4C5D2E4'. For this problem, you can falsely "compress" strings of single or double letters. For instance, it is okay for 'AAB' to return 'A2B1' even though this technically takes more space.

The function should also be case sensitive, so that a string 'AAAaaa' returns 'A3a3'.

[String Compression problem](./problem_string_compression.ipynb)

---

### Unique Characters in String

Given a string,determine if it is compreised of all unique characters. For example, the string 'abcde' has all unique characters and should return True. The string 'aabcde' contains duplicate characters and should return false.

[Unique Characters problem](./problem_unique_characters.ipynb)

---

[TOP](#dsa---array)
