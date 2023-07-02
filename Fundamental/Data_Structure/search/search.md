# DSA - Search

[back](../data_structure.md)

- [DSA - Search](#dsa---search)
  - [Sequential Search](#sequential-search)
    - [Implement Sequential Search in Python](#implement-sequential-search-in-python)
      - [Unordered List](#unordered-list)
      - [Unordered List](#unordered-list-1)
  - [Binary Search](#binary-search)
    - [Implement Sequential Search in Python](#implement-sequential-search-in-python-1)
      - [Iterative Way](#iterative-way)
      - [Recursive Way](#recursive-way)

---

## Sequential Search

- `Sequential Search`

  - sequentially go through the data structure, comparing elements as you go along.

- Unordered List

  - Stop Condition:
    - found
    - index > len - 1

  | Case                 | Best Case | Worst Case | Averaage Case |
  | -------------------- | --------- | ---------- | ------------- |
  | target presented     | 1         | n          | n/2           |
  | target not presented | n         | n          | **n**         |

- Ordered List:

  - only have search until we reach an element which is a **match** or we reach an element which is **greater than** our search target.
  - Stop Condition:
    - found
    - array[index]>target
    - index > len - 1

  | Case                 | Best Case | Worst Case | Averaage Case |
  | -------------------- | --------- | ---------- | ------------- |
  | target presented     | 1         | n          | n/2           |
  | target not presented | n         | n          | **n/2**       |

---

### Implement Sequential Search in Python

#### Unordered List

```py
def seq_search(arr,ele):
    """
    General Sequential Search. Works on Unordered lists.
    """

    # Start at position 0
    pos = 0
    # Target becomes true if ele is in the list
    found = False

    # go until end of list
    while pos < len(arr) and not found:

        # If match
        if arr[pos] == ele:
            found = True

        # Else move one down
        else:
            pos  = pos+1

    return found
```

---

#### Unordered List

```py
def ordered_seq_search(arr,ele):
    """
    Sequential search for an Ordered list
    """
    # Start at position 0
    pos = 0

    # Target becomes true if ele is in the list
    found = False

    # Stop marker
    stopped = False

    # go until end of list
    while pos < len(arr) and not found and not stopped:

        # If match
        if arr[pos] == ele:
            found = True

        else:

            # Check if element is greater
            if arr[pos] > ele:
                stopped = True

            # Otherwise move on
            else:
                pos  = pos+1

    return found

```

---

## Binary Search

- `Binary Search`
  - A binary search will start by examining the **middle item**.
  - If that item is the one we are searching for, we are done.
  - If the item we are searching for is **greater** than the middle item, we know that the entire lower half of the list as well as the middle item can be eliminated from further consideration.
    - The item, if it is in the list, must be in the **upper half.**
  - Each comparison eliminates about half of the remaining items from consideration.

| Comparison | Approximate Number of Item Left |
| ---------- | ------------------------------- |
| 1          | `n/2`                           |
| 2          | `n/4`                           |
| ...        | ...                             |
| i          | `n/(2**i)`                      |

---

### Implement Sequential Search in Python

#### Iterative Way

```py
def binary_search(arr,ele):

    # First and last index values
    first = 0
    last = len(arr) - 1

    found = False


    while first <= last and not found:

        mid = (first+last)//2

        # Match found
        if arr[mid] == ele:
            found = True

        # Set new midpoints up or down depending on comparison
        else:
            # Set down
            if ele < arr[mid]:
                last = mid -1
            # Set up
            else:
                first = mid + 1

    return found
```

---

#### Recursive Way

```py
def rec_bin_search(arr,ele):

    # Base Case!
    if len(arr) == 0:
        return False

    # Recursive Case
    else:

        mid = len(arr)//2

        # If match found
        if arr[mid]==ele:
            return True

        else:

            # Call again on second half
            if ele<arr[mid]:
                return rec_bin_search(arr[:mid],ele)

            # Or call on first half
            else:
                return rec_bin_search(arr[mid+1:],ele)
```

---


[TOP](#dsa---search)
