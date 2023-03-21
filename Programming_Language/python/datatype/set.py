print("\n---------Keep All, But NOT the Duplicates--------\n")
# symmetric_difference_update()
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

x.symmetric_difference_update(y)    # update x

print(x)        # {'microsoft', 'google', 'banana', 'cherry'}


# symmetric_difference()
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

z = x.symmetric_difference(y)       # return a new set

print(z)        # {'microsoft', 'google', 'banana', 'cherry'}


x = {"apple", "banana", "cherry", True}
y = {"google", 1, "apple", 2}
z = x.symmetric_difference(y)       # {2, 'banana', 'google', 'cherry'}

print(z)


## Check if Item Exists:`in`

xlist = {"apple", "banana", "cherry"}
if "apple" in xlist:
  print("Yes, 'apple' is in the fruits list")

