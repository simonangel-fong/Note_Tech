print("\n--------Immutable--------")

xVar = 'abc'
print(id(xVar))

xVar = 'xyz'
print(id(xVar))

# 在内存中的地址不同, 显示xVar先后指向的不是相同的对象.
