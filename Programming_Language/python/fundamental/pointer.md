# Python - Pointer

[Back](../index.md)

- [Python - Pointer](#python---pointer)
  - [Pointer](#pointer)
  - [浅拷贝: `=` and `copy()`](#浅拷贝--and-copy)
  - [深拷贝: 使用 `deepcopy()` 函数](#深拷贝-使用-deepcopy-函数)
  - [不可变对象(如元组)中的指针](#不可变对象如元组中的指针)
  - [Python 中的 immutable 对象](#python-中的-immutable-对象)

---

## Pointer

- **Python 引用计数机制**

  - Python 是自动管理内存的，它采用“引用计数”的方式管理内存，即 Python 内部会记录对象有多少个引用，
    - 如果某个对象的引用计数**大于 0**，该对象就会一直**存放在内存中**；
    - 当对象的引用计数**为 0 时**，就会被垃圾回收机制**回收**。
  - 这也是 Python 的方便之处，开发者无需考虑提前为对象分配内存，使用完后也无需手动释放内存。

- **命名空间**

  - Python 中的**命名空间**指的是一个作用域中所有变量、关键字和函数组成的列表，用于避免命名冲突，不同命名空间中可以包含相同的变量名。
  - 例如，每个命名空间中都有内置函数(如 print()和 str())，关键字(如 None 和 True)。
  - 当你创建一个新变量时，变量名会被添加到其所在作用域的命名空间中。例如，下面的代码会把变量名 my_string 添加到全局命名空间中:
    - `my_string = "Hello World!"`

- 指针

  - 指针就是**变量名**——也就是 Python 命名空间的入口——与 Python 内存中的对象相对应。
  - 在上面的例子中，指针就是 **my_string**，内存中的对象是“Hello World!”字符串。通过在命名空间中使用指针，我们就能访问和操作内存中的对象了。
  - 就像一个人可能有多个名字一样，**多个指针也可能会指向同一个对象**。

- 例子
  - `my_list：my_list = ['string', 42]`
  - 变量名 my_list 指向的是列表对象。列表对象**有 2 个指针**，分别指向其中的 2 个元素。
  - 由此可以看出，当创建一个列表时，如果其中有元素，那么**该列表也会包含指针，指向这些元素**。

---

## 浅拷贝: `=` and `copy()`

```py
print("\n--------original list--------")
a = ["string", 42]
print("a", a)    # ["string", 42]


print("\n--------reference--------")
b = a
b[0] = "some words"
print("a", a)    # ['some words', 42]
print("b", b)    # ['some words', 42]


print("\n--------copy list--------")
c = a.copy()
c[0] = "hello!"
print("a", a)     # ['some words', 42]
print("b", b)     # ['some words', 42]
print("c", c)     # ['hello!', 42]

```

- a 之所以会发生改变，是因为 b = a 并没有创建一个新的列表，**只是创建了一个新的指针 b**，它与 a 指向了相同的列表。

- 使用 copy 方法
  - 创建一个新的列表，同时包含新的指针，但这些指针指向的元素与原列表相同
  - 即`=`引用使用相同的指针, 当 b 通过指针修改指向的元素时, 因为 a 的指针与 b 的指针相同, 所以 a 指向的元素也会受影响;
  - 使用`copy()`方法会生成新的指针, 当 c 修改指针指向的元素时,由于 c 与 a,b 的指针不相同, 所以 c 指向的元素不会影响 a, b.

```py
print("\n--------original list--------")
a = [["alex", "beth"]]
print("a", a)    # a [['alex', 'beth']]


print("\n--------copy list--------")
b = a.copy()
b[0].append("charlie")
print("a", a)    # a [['alex', 'beth', 'charlie']]
print("b", b)    # b [['alex', 'beth', 'charlie']]

```

- a[0]的元素也变了. 其原因是`copy`方法是浅拷贝。a[0]与 b[0]指向了同一个对象
  - 即 copy 方法保证指针不同, 但当指针指向的元素对象是可变对象且发生改变时, 如上例中`a[0]`和`b[0]`共同指向的, 该`["alex", "beth"]`在`b[0]`发生改变时, 也会影响到`a[0]`

---

## 深拷贝: 使用 `deepcopy()` 函数

```py
print("\n--------deepcopy()--------")

from copy import deepcopy
a = [["alex", "beth"]]
c = deepcopy(a)
c[0].append("dan")

print('a', a)       # a [['alex', 'beth']]
print('c', c)       # c [['alex', 'beth', 'dan']]
```

- deepcopy 函数采用递归的方式，复制每一个对象，避免指针混叠
  - 即保证指针和被指向的对象都不相同.
  - 当上例中`c[0]`修改指向对象时, 因为是深拷贝,指针和指向的对象都不同, 所以 a 与 c 不会发生影响.

---

## 不可变对象(如元组)中的指针

```py
print("\n--------list--------")

b = [42, 'beeblebrox']

b[0] = 63
b[1] = 'beeble'

print(b)        # [63, 'beeble']


print("\n--------tuple--------")

xVar = 'abc'
yVar = [0, 1]
a = (42, 'beeblebrox', xVar, [1, 2], yVar)

# a[0] = 63       # TypeError: 'tuple' object does not support item assignment
# a[1] = 'beeble'     # TypeError: 'tuple' object does not support item assignment
# a[2] = 'beeble'     # TypeError: 'tuple' object does not support item assignment
a[3].append(3)
xVar = 'xyz'
yVar.pop()

print(a)        # (42, 'beeblebrox', 'abc', [1, 2, 3], [0])

```

- 列表的可变性

  - 指针可变

- 元组不可变

  - 之所以说它不可变，是因为当创建 a 时，它的所有指针都是固定的, `a[0]`, `a[1]`...
  - 即指针不可变, 即只能固定指向一个元素
    - 假如元素是不可变的则无法修改, 如上例的`a[0]`、`a[1]`
    - 如果元素是可变, 则可以修改, 如上例的`a[3]`. 但不是通过改变指针, 而改变指向的元素(.append())

- 可改变对象 / 不可改变对象
  - 上例中`a[2]`指向变量`xVar`, 该变量指向的是字符串, 不可改变对象. 所以当 xVar 的值改变为`xyz`时, `a[2]`依然指向`abc`
  - 上例中`a[3]`指向变量`yVar`, 变量指向的是列表, 可改变对象,所以当 yVar 的值改变时, `a[3]`的值也会改变.

---

## Python 中的 immutable 对象

- Immutable object

  - int
  - float
  - str
  - bool
  - tuple

- 注意 Immutable 的是对象, 不是变量. 变量是指向对象的指针.指针可以改变, 但不可变对象一旦创建则不会改变.

```py
print("\n--------Immutable--------")

xVar = 'abc'
print(id(xVar))

xVar = 'xyz'
print(id(xVar))

# 在内存中的地址不同, 显示xVar先后指向的不是相同的对象.
```

- 上例中
  - 改变的是 xVar 变量指向的对象, 即改变的是指针.
  - `'abc'`和`'xyz'`在内存中有不同的地址, 即 xVar 变量前后指向不同的对象
  - str 是不可变对象, 一旦在内存中创建则不能改变.
  - 因为 python 的引用计数机制, 一旦不可变对象没有被引用, 即引用的指针数量为 0 时, 会被垃圾回收机制回收, 释放内存.

---

[TOP](#python---pointer)
