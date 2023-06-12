# DSA - Big O

[Back](./index.md)

- [DSA - Big O](#dsa---big-o)
  - [Big O Notation](#big-o-notation)
  - [Space Complexity](#space-complexity)
  - [Best Case, Average Case, and Worst Case](#best-case-average-case-and-worst-case)
  - [Common Big-O](#common-big-o)
    - [`O(n)`: Linear / Proportional](#on-linear--proportional)
    - [`O(n^2)`: Quadratic / Loop within a loop](#on2-quadratic--loop-within-a-loop)
    - [`O(1)`: Constant](#o1-constant)
    - [`O(log(n))`: Divide and Conquer](#ologn-divide-and-conquer)
  - [Big O Analysis](#big-o-analysis)
    - [Drop Constants](#drop-constants)
    - [Drop Non-Dominants](#drop-non-dominants)
    - [Different Terms for Inputs](#different-terms-for-inputs)
  - [Big O of List](#big-o-of-list)
  - [Big-O Cheat Sheet](#big-o-cheat-sheet)

---

## Big O Notation

- **Analyze algorithms**

  - compare the amount of **space** they take in memory
  - compare how much **time** it takes each function to run.
  - However, we can not use **"time to run"** as an objective measurement, because that will depend on the **speed of the computer itself and hardware capabilities.**
  - A good place to start would be to compare the number of assignments each algorithm makes, **Big-O**!

- `Big-O notation`

  - describes **_how quickly runtime will grow relative to the input as the input get arbitrarily large_**.

- Remember, we want to **_compare how quickly runtime will grows_**, _not compare exact runtimes_, since those can vary depending on hardware.

- Since we want to compare for a variety of input sizes, we are **only concerned with runtime grow _relative_ to the input.** This is why we use `n` for notation.

- As `n` gets arbitrarily large we **only worry about terms that will grow the fastest as `n` gets large**, to this point.
  - `Big-O` analysis is also known as **asymptotic analysis**

---

## Space Complexity

- The notation of **space complexity** is the same, but instead of checking the time of operations, we check **the size of the allocation of memory.**

---

## Best Case, Average Case, and Worst Case

| Geek Letter  | Notation     |
| ------------ | ------------ |
| `Ω`(Omiga)   | Best Case    |
| `θ`(theta )  | Average Case |
| `O`(Omikron) | Worst Case   |

- When talking about `big O`, it is usually talking about **worst case**.

---

## Common Big-O

| Big-O        | Name        |
| ------------ | ----------- |
| `O(1)`       | Constant    |
| `O(log(n))`  | Logarithmic |
| `O(n)`       | Linear      |
| `O(nlog(n))` | Log Linear  |
| `O(n^2)`     | Quadratic   |
| `O(2^n)`     | Exponential |

![diagram](./pic/Big-O%20Complexity%20Chart.png)

- Clearly we want to choose algorithms that **stay away from any exponential, quadratic, or cubic behavior!**

- When it comes to `Big O notation` we _only care about the most significant terms_, remember as the input grows larger **only the fastest growing terms will matter.**

---

### `O(n)`: Linear / Proportional

- The function runs in **O(n) (linear time)**.

  - This means that the number of operations taking place scales **linearly with n**

- 图像上, 随着`n`的增加, number of operation`O(n)`呈现线性增长.

```py
def print_items(n):
    '''
    Takes n operations for a specific input n
    '''
    for i in range(n):
        print(i)

func_lin(10)

```

---

### `O(n^2)`: Quadratic / Loop within a loop

- The function performs `n` operations for _every item in the list!_

- This means in total, we will perform `n` times `n` assignments, or `n^2`.
- You can see how dangerous this can get for very large inputs! This is why Big-O is so important to be aware of!
- `O(n*n) = O(n^2)`

```py

def print_items(lst):
    for i in range(n):
        for j in range(n):
            print(i, j)

print_items(10)
```

---

### `O(1)`: Constant

- The function is constant because regardless of the list size, the function will **only ever take a constant step size.**
- The most efficient `Big O`

```py
def add_items(n):
    return n + n + n

add_items(10)
```

---

### `O(log(n))`: Divide and Conquer

- 简化的推导过程:

  - 使用 binary search 时, 每次都二分所有元素.
  - 所以 worst case 下的方程是`Big O = log(n)`, 注意该处 log 的底是 2.
  - 即在自然数范围内对 n 取底为 2 的对数, 其最大值即`Big O`(worst case)
  - `2^Big(O)` => `Big O = log(n)` => `O(log(n))`

- A very efficient `Big O`. Flat and close to `O(1)`

---

## Big O Analysis

### Drop Constants

- `Drop Constants`

  - A simplification technique of Big O.
  - 由于只关注 input 对 number of operations 的显著影响, 所以常数系数被忽略.
  - `O(n) + O(n) = O(n+n) = O(2n) = O(n)`

```py
def print_items(n):
    for i in range(n):
        print(i)

    for j in range(n):
        print(j)

print_items(10)
# 对每个operation都执行两次, 所以time complexity是O(2n), 分析时看作是O(n)

```

---

### Drop Non-Dominants

- `Drop Non-Dominants`
  - A simplification technique of Big O.
  - 由于只关注显著的影响, 所以非显著的影响将会被忽略
  - `O(n^2) + O(n) = O(n^2 + n) = O(n^2)`

```py
def print_items(n):
  # O(n^2)
    for i in range(n):
        for j in range(n):
            print(i,j)

  # O(n)
    for k in range(n):
        print(k)

print_items(10)
```

---

### Different Terms for Inputs

- 分析时, 参数一般是一个 n; 但当参数是多个时, 不适用 Drop Constants.
- 以下代码为例, 其`Big O`是`O(a)+O(b) = O(a+b)`, 不能再简化.因为参数有两个, 不能直接简化为`O(2n)`

```py
def print_items(a,b):
    for i in range(a):
        print(i)

    for j in range(b):
        print(j)

print_items(1, 10)
```

- 如果以上代码是 a 与 b 嵌套循环时, 其`big O`是`O(a)*O(b) = O(a*b)`

---

## Big O of List

- List is a built-in data structure in Python.

  - Adding and Removing item at the **end** of a list: `O(1)`
  - Adding and Removing item at the **front** of a list: `O(n)`
  - Looking for a value with index of a list: `O(1)`

| Operation          | Big O  | Description               |
| ------------------ | ------ | ------------------------- |
| `.append()`        | `O(1)` |                           |
| `.pop()`           | `O(1)` |                           |
| `.insert(0,value)` | `O(n)` | re-indexing               |
| `.pop(0)`          | `O(n)` | re-indexing               |
| `list[index]`      | `O(1)` | look for value with index |

---

## Big-O Cheat Sheet

[Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

- Common Data Structure

  - 注意: 以上的 space 复杂度几乎都是`O(n)`, 所以现实中一般注重 time 复杂度.
    ![Common Data Structure](./pic/Common%20Data%20Structure%20Operations.png)

- Array Sorting Algorithms

  - 对几乎 sorted 的数组, Bubble sort 和 Insertion sort 的 best case 都是 Ω(n), 比其他 sort 都有效率.
  - Quick Sort, Merge Sort 的 space 复杂度都不如 Bubble sort, Insertion sort, selection sort.
  - Quick sort, merge sort 的 worst case 有些许优势, 但对几乎 sorted 的数组, 效率没有优势.

  ![Array Sorting Algorithms](./pic/Array%20Sorting%20Algorithms.png)

---

[TOP](#python---data-structure--algorithms)
