print("\n--------- setattr(object, attribute, value) --------\n")


class Person:
    name = "John"
    age = 36
    country = "Norway"


print(getattr(Person, 'age'))   # 36

setattr(Person, 'age', 40)
print(getattr(Person, 'age'))   # 40
