# Data Structure - Array

[Back](../index.md)

---

- [Data Structure - Array](#data-structure---array)
  - [Static Array](#static-array)
  - [Dynamic Array](#dynamic-array)
  - [Dynamic Array - Java](#dynamic-array---java)

---

## Static Array

- `Static Array`:

  - a fixed length container containing n elements indexable from the range [0,n-1]

- indexable:

  - each slot/index in the array can be referenced with a number.

- Usage

  - 1. Storing and accessing **sequential data**
  - 2. **Temporarily** storing objects
  - 3. Used by **IO** routines as buffers
  - 4. **Lookup tables** and inverse lookup tables
  - 5. Can be used to **return** multiple values from a function
  - 6. Used in **dynamic programming** to cache answers to subproblems

- Complexity

  |           | Static Array | Dynamic Array |
  | --------- | ------------ | ------------- |
  | Access    | O(1)         | O(1)          |
  | Search    | O(n)         | O(n)          |
  | Insertion | N/A          | O(n)          |
  | Appending | N/A          | O(1)          |
  | Deletion  | N/A          | O(n)          |

- Elements in a static array are referenced by their index.

  - There is no other way to access elements in an array.

- Array indexing is `zero-based`, meaning the first element is found in position zero.

---

## Dynamic Array

- The `dynamic array` can **grow** and **shrink** in size.

- How can we implement a dynamic array?
  - A: One way is to use a static array!
    - 1. Create a static array with an initial capacity.
    - 2. Add elements to the underlying static array, keeping track of the number of elements.
    - 3. If adding another element will exceed the capacity, then create a new static array with twice the capacity and copy the original elements into it.

---

## Dynamic Array - Java

- DynamicArray.java

```java
package Array;

import java.util.*;

public class DynamicArray<T> implements Iterable<T> {

    private int size;// external array size
    private int capacity;// internal array size
    private T[] arr;

    public DynamicArray() {
        this(10);
    }

    public DynamicArray(int initSize) {
        if (initSize < 0) {
            throw new IllegalArgumentException("Argument cannot be less than zero.");
        } else {
            this.capacity = initSize;
            arr = (T[]) new Object[initSize];

        }
    }

    public int size() {
        return this.size;
    }

    public boolean isEmpty() {
        return this.size == 0;
    }

    public int indexOf(T obj) {
        for (int i = 0; i < size; i++) {
            // System.out.println(obj);
            if (obj == null && arr[i] == null) {
                return i;
            }

            if (obj != null && obj.equals(arr[i])) {
                return i;
            }
        }
        return -1;
    }

    public boolean contain(T obj) {
        return indexOf(obj) != -1;
    }

    public void add(T obj) {

        // when capacity is not enough, then resize.
        if (size + 1 > capacity) {
            if (capacity == 0) {// when capacity is zero.
                capacity = 1;
            } else {
                capacity *= 2;// double cap
            }

            T[] newArr = (T[]) new Object[capacity];
            for (int i = 0; i < size; i++) {
                newArr[i] = arr[i];
            }
            arr = newArr;
        }
        arr[size] = obj;
        size += 1;
    }

    public T get(int index) {
        if (index < 0 || index >= this.size) {
            throw new IndexOutOfBoundsException();
        } else {
            return arr[index];
        }
    }

    public void set(int index, T obj) {
        if (index < 0 || index >= this.size) {
            throw new IndexOutOfBoundsException();
        } else {
            arr[index] = obj;
        }
    }

    public void clear() {
        size = capacity = 0;
        arr = (T[]) new Object[capacity];
    }

    public T removeAt(int index) {
        if (index < 0 || index >= this.size) {
            throw new IndexOutOfBoundsException();
        }
        T data = arr[index];

        T[] newArr = (T[]) new Object[this.size - 1];
        for (int i = 0, j = 0; i < size; i++, j++) {// i for old arr, j for new arr
            if (i == index) {
                j -= 1; // when i == index, j deduct one
            } else {
                newArr[j] = arr[i]; // otherwise, copy item
            }

        }
        arr = newArr;
        size -= 1;
        capacity = size;

        return data;
    }

    public boolean remove(T obj) {
        int index = indexOf(obj);
        if (index == -1) {
            return false;
        } else {
            removeAt(index);
            return true;
        }
    }

    @Override
    public Iterator<T> iterator() {
        // using anonymous method
        return new Iterator<T>() {
            int index = 0;

            @Override
            public boolean hasNext() {
                return index < size;
            }

            @Override
            public T next() {
                return arr[index++];// return value at index; then index +1;
            }

        };
    }

    @Override
    public String toString() {
        if (size == 0) {
            return "[]";
        } else {
            StringBuilder result = new StringBuilder(size).append("[");
            for (int i = 0; i < size - 1; i++) {// loop to size-1, because of the comma
                result.append(arr[i] + ", ");
            }

            return result.append(arr[size - 1] + "]").toString();
        }
    }

}

```

- DynamicArrayDemo.java

```java
package Array;

import java.util.*;

public class DynamicArrayDemo {
    public static void main(String[] args) {

        System.out.println("\n--------Test DynamicArray--------\n");

        DynamicArray<Integer> arrInt = new DynamicArray<Integer>();
        System.out.println(arrInt.size());

        System.out.println(arrInt.isEmpty());

        arrInt.add(0);
        arrInt.add(1);
        arrInt.add(2);
        arrInt.add(3);
        arrInt.add(4);

        System.out.println("\n--------create-------");

        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("toString():\t" + arrInt);
        System.out.println("get():\t\t" + arrInt.get(4));
        System.out.println("indexOf():\t" + arrInt.indexOf(5));
        System.out.println("contain():\t" + arrInt.contain(4));

        System.out.println("\n--------update--------");
        arrInt.set(4, 5);
        System.out.println("Ater set():\t" + arrInt);

        System.out.println("\n--------clear--------");
        arrInt.clear();
        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("toString():\t" + arrInt);

        System.out.println("\n--------add--------");
        arrInt.add(10);
        arrInt.add(20);
        arrInt.add(30);
        arrInt.add(40);
        arrInt.add(50);
        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("new add():\t" + arrInt);

        System.out.println("\n--------removeAt--------");
        System.out.println("removeAt():\t" + arrInt.removeAt(0));
        System.out.println("toString():\t" + arrInt);
        System.out.println("size():\t\t" + arrInt.size());

        System.out.println("\n--------remove--------");
        System.out.println("remove():\t" + arrInt.remove(10));
        System.out.println("remove():\t" + arrInt.remove(40));
        System.out.println("toString():\t" + arrInt);
        System.out.println("size():\t\t" + arrInt.size());

        System.out.println("\n--------iterator--------");
        Iterator<Integer> itr = arrInt.iterator();
        while (itr.hasNext()) {
            System.out.println(itr.next());
        }

    }
}

```

---

[TOP](#data-structure---array)
