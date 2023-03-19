# String
print("\n--------String--------\n")
print(bool("Hello"))    # True
print(bool(" "))    # True
print(bool(""))    # False


# Number
print("\n--------Number--------\n")
print(bool(15))     # True
print(bool(0.1))     # False
print(bool(0))     # False
print(bool(0.0))     # False
x, y = 100, 0
print(bool(x*y))     # False


# list
print("\n--------List--------\n")
print(bool(list()))     # False
print(bool([]))     # False
print(bool(["a"]))     # True


# tuple
print("\n--------Tuple--------\n")
print(bool(tuple()))     # False
print(bool(()))     # False
print(bool(("a")))     # True

# set
print("\n--------Set--------\n")
print(bool(set()))     # False
print(bool({}))     # False
print(bool(set([0, 1, 2, 3, 4])))     # True
print(bool({"a"}))     # True


# dict
print("\n--------Dict--------\n")
print(bool(dict()))     # False
print(bool({}))     # False
print(bool({"year": 1980}))     # True


# object
print("\n--------Object--------\n")


class myclass01():
    def __len__(self):
        return 0


myobj = myclass01()
print(bool(myobj))  # False


class myclass02():
    def __len__(self):
        return 1


myobj = myclass02()
print(bool(myobj))  # True


# function
print("\n--------function--------\n")


def myfunction():
    return True


print(myfunction())     # True


# isinstance()
print("\n--------isinstance() function--------\n")
x = 200
print(isinstance(x, int))       # True
print(isinstance(x, float))       # False


# others
print("\n--------others--------\n")
print(bool(False))     # False
print(bool(None))     # False
