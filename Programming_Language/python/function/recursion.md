# Python - Recursion

[Back](../index.md)

- [Python - Recursion](#python---recursion)
  - [Recursion 递归](#recursion-递归)
  - [Factorial function](#factorial-function)
  - [Factorial function in Python:](#factorial-function-in-python)
  - [Summary](#summary)
  - [Problems](#problems)
    - [Cumulative Sum](#cumulative-sum)
    - [sum of all digits](#sum-of-all-digits)
    - [Split string into words](#split-string-into-words)
  - [Memoization](#memoization)
    - [Implement memoization in Python](#implement-memoization-in-python)
    - [Problems](#problems-1)
  - [Further Reading](#further-reading)

---

## Recursion 递归

- Two main instances of `Recursion`.

  - 1. a **technique** in which a **function** makes one or more **calls to itself**.在数学与计算机科学中，是指在函数的定义中使用函数自身的方法。
  - 2. a **data structure** uses smaller instances of the exact same type of data structure when it represents itself.

- `Recursion` actually occurs in the real world, such as `fractal`阶乘 patterns seen in plants!

- Advantage
  - Recursion provides a powerful **alternative for performing repetitions of tasks** in which a **loop is not ideal**.
  - Most modern programming languages support recursion and recursion serves as a great tool **for building out particular data structures**.

---

## Factorial function

- `Factorial function` is denoted **with an exclamation point** and is defined as the **product** of the integers from 1 to _n_.

- Formally, we can state this as:

  $$ n! = n·(n-1)·(n-2)... 3·2·1 $$

  - Note, **if n = 0, then n! = 1**. This is important to take into account, because it will serve as our `base case`.

- `Base case`

  - the **exit strategy** of recursion

- A proper `recursive function` **must** always have **a** `base case`:

  - The base case is **a way to return** without making a recursive call. In other words, it is the **mechanism that stops** this process of ever more recursive calls and an ever growing stack of function calls waiting on the return of other function calls. 在代码实现中, 先判断是否 base case. 如果是, 函数直接返回; 否则才开始递归

  - Therefore, we should make sure that every function call **eventually hits the base case** in order **to avoid infinite recursion**. Once we hit it, we can start taking function calls off the top of the stack and returning from them.

- can rewrite the formal recursion definition in terms of recursion like so:

  $$ n! = n·(n−1)!$$

  - Note, **if n = 0, then n! = 1**. This means the **base case** occurs once n=0, the _recursive cases_ are defined in the equation above.

---

## Factorial function in Python:

```py
def fact(n):
    '''
    Returns factorial of n (n!).
    Note use of recursion
    '''
    # BASE CASE!
    if n == 0:
        return 1

    # Recursion!
    else:
        return n * fact(n-1)
```

---

## Summary

- 三部分:

  - 1. 处理 recursive condition
  - 2. base case
  - 3. recursive case

- 关键: 参数 n 在相邻递归时的关系

- 思考顺序:

  - base case
  - recursive case
    - recursive 的参数
  - 是否需要传递值

- 递归之间传递数据:

  ```py
  def func(output = None):

    # 初次递归时, output为none
    if not output:
        output = []
    # some code
    if condition:
        output.append()

    return output
  ```

- 对遍历递归:

  ```py
  def func(loop_target, output = None):

    if output is None:
        output = []

    for item in loop_target:
        if condition:
            output.append(item)
            return func(loop_target[len(item)], output)

    return output
  ```

---

## Problems

[Problems](./problem_recursion.ipynb)

### Cumulative Sum

**Write a recursive function which takes an integer and computes the cumulative sum of 0 to that integer**

**For example, if n=4 , return 4+3+2+1+0, which is 10.**

This problem is very similar to the factorial problem presented during the introduction to recursion. Remember, always think of what the base case will look like. In this case, we have a base case of n =0 (Note, you could have also designed the cut off to be 1).

In this case, we have:
n + (n-1) + (n-2) + .... + 0

Fill out a sample solution:

```py
def rec_sum(n):
    pass
```

---

### sum of all digits

**Given an integer, create a function which returns the sum of all the individual digits in that integer. For example:**

- if n = 4321, return 4+3+2+1

```py
def sum_func(n):
    pass
```

---

### Split string into words

_Note, this is a more advanced problem than the previous two! It aso has a lot of variation possibilities and we're ignoring strict requirements here._

Create a function called word_split() which takes in a string **phrase** and a set **list_of_words**. The function will then determine if it is possible to split the string in a way in which words can be made from the list of words. You can assume the phrase will only contain words found in the dictionary if it is completely splittable.

```py

def word_split(phrase, list_of_words, output=None):
    pass

word_split('themanran', ['the', 'ran', 'man'])

```

---

## Memoization

- `Memoization / Memoisation`

  - an **optimization technique** used primarily to **speed up computer programs** by **storing** the results of expensive function calls and **returning** the cached result when the **same** inputs occur again.

- `Memoization` is a way to lower a function's **time cost** in exchange for **space cost**; that is, memoized functions become optimized **for speed** in exchange for a higher use of **computer memory space**.

- `computational complexity`

  - The **time/space "cost"** of algorithms
  - All functions have a computational complexity in time (i.e. they take time to execute) and in space.

- Although a space–time tradeoff occurs (i.e., space used is speed gained), this differs from some other optimizations that involve time-space trade-off, such as strength reduction, in that **memoization is a run-time** rather than compile-time optimization.

- Moreover, strength reduction potentially replaces a costly operation such as multiplication with a less costly operation such as addition, and the results in savings can be highly machine-dependent (non-portable across machines), whereas **memoization is a more machine-independent, cross-platform strategy**.

- **Non-memoized** implementation of factorial

        function factorial (n is a non-negative integer)
            if n is 0 then
                return 1 [by the convention that 0! = 1]
            else
                return factorial(n – 1) times n [recursively invoke factorial
                                                with the parameter 1 less than n]
            end if
        end function

- **Memoized** implementation of factorial

        function factorial (n is a non-negative integer)
            if n is 0 then
                return 1 [by the convention that 0! = 1]
            else if n is in lookup-table then
                return lookup-table-value-for-n
            else
                let x = factorial(n – 1) times n [recursively invoke factorial
                                                with the parameter 1 less than n]
                store x in lookup-table in the nth slot [remember the result of n! for later]
                return x
            end if
        end function

- Keep this in mind when working on the **Coin Change Problem**投硬币 and the **Fibonacci Sequence**112358 Problem.

---

### Implement memoization in Python

```py
# encapsulate the memoization process into a class:
# 创建一个类, 该类的实例将会存储一个函数和字典
# 调用该实例时, 将先在字典中查找其参数; 如果没有则计算并存储在字典;如果有则直接返回其值.
class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

# factorial function
def factorial(k):

    if k < 2:
        return 1

    return k * factorial(k - 1)

# create an instance of memoization
# 此时factorial是被重写, 但之前的定义匿名存储在Memoize的实例属性f中.
factorial = Memoize(factorial)

print(factorial(3))     # 6

```

---

### Problems

[Practice](./problem_recursion.ipynb)

---

## Further Reading

http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html

https://www.quora.com/Why-is-tail-recursion-optimisation-not-implemented-in-languages-like-Python-Ruby-and-Clojure-Is-it-just-difficult-or-impossible

---

[TOP](#python---recursion)
