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
