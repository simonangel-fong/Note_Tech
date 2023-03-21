# Escape Character

# region Case sensitive

print("\n--------capitalize()--------\n")
# capitalize(): returns a string where the first character is upper case, and the rest is lower case.
print("HELLO WORLD", ":", "HELLO WORLD".capitalize())   # Hello world
print("hello world", ":", "hello world".capitalize())   # Hello world
print("straße", ":", "straße".capitalize())  # Straße


print("\n--------casefold()--------\n")
# Converts string into lower case
print("HELLO WORLD", ":", "HELLO WORLD".casefold())   # Hello world
print("hello world", ":", "hello world".casefold())   # Hello world
print("Straße", ":", "Straße".casefold())  # strasse


print("\n--------lower()--------\n")
# Converts string into lower case
print("HELLO WORLD", ":", "HELLO WORLD".lower())   # hello world
print("hello world", ":", "hello world".lower())   # hello world
print("Straße", ":", "Straße".lower())  # straße

# endregion

# region Style
print("\n--------center()--------\n")
# center align the string, using a specified character (space is default) as the fill character.
# length	Required. The length of the returned string
# character	Optional. The character to fill the missing space on each side. Default is " " (space)
print("banana", "|", "banana".center(20), "|")   # hello world
print("banana", "|", "banana".center(20, "*"), "|")   # *******banana*******
print("hello world", "|", "hello world".center(20), "|")   # hello world
print("hello world", "|", "hello world".center(
    20, "*"), "|")   # ****hello world*****


# endregion

print("\n--------count()--------\n")
# returns the number of times a specified value appears in the string.
# value	Required. A String. The string to value to search for
# start	Optional. An Integer. The position to start the search. Default is 0
# end	Optional. An Integer. The position to end the search. Default is the end of the string
print("banana", "banana".count("a"))   # 3
print("banana", "banana".count("aa"))   # 0
print("banana", "banana".count("an"))   # 2
print("Hello World", ":", "Hello World".count("o"))   # 2
print("Hello World", ":", "Hello World".count("o", 5, 8))   # 1


print("\n--------endswith()--------\n")
# returns True if the string ends with the specified value, otherwise False.
# value	Required. The value to check if the string ends with
# start	Optional. An Integer specifying at which position to start the search
# end	Optional. An Integer specifying at which position to end the search
print("banana", "banana".endswith("na"))   # True

print("Hello World", ":", "Hello World".endswith("lo"))   # False
print("Hello World", ":", "Hello World".endswith("World"))   # True

print("Hello World", ":", "Hello World".endswith("llo"))   # False
print("Hello World", ":", "Hello World".endswith("llo", 0, 5))   # True


print("\n--------expandtabs()--------\n")
# sets the tab size to the specified number of whitespaces.
# Parameter Description
# tabsize	Optional. A number specifying the tabsize. Default tabsize is 8
print("H\te\tl\tl\to")   # H       e       l       l       o
print("H\te\tl\tl\to".expandtabs())   # H       e       l       l       o
print("H\te\tl\tl\to".expandtabs(0))   # Hello
print("H\te\tl\tl\to".expandtabs(2))   # H e l l o
print("H\te\tl\tl\to".expandtabs(4))   # H   e   l   l   o


print("\n--------find()--------\n")
# finds the first occurrence of the specified value.
# returns -1 if the value is not found.
# Parameter Description
# value     Required. The value to search for
# start     Optional. Where to start the search. Default is 0
# end       Optional. Where to end the search. Default is to the end of the string
print("Hello World",  "Hello World".find(""))       # 0
print("Hello World",  "Hello World".find("a"))      # -1
print("Hello World",  "Hello World".find("W"))      # 6
print("Hello World",  "Hello World".find("l"))      # 2
print("Hello World",  "Hello World".find("ll"))     # 2
print("Hello World",  "Hello World".find("l", 2))   # 2, inclusive
print("Hello World",  "Hello World".find("l", 3))   # 3
print("Hello World",  "Hello World".find("l", 4))   # 9
print("Hello World",  "Hello World".find("l", 4, 8))   # -1
print("Hello World",  "Hello World".find("l", 4, 9))   # -1, exclusive
print("Hello World",  "Hello World".find("l", 4, 10))   # 9


print("\n--------format()--------\n")
# formats the specified value(s) and insert them inside the string's placeholder.
# The placeholder is defined using curly brackets: {}.
# returns the formatted string.
# 1. The placeholders can be identified using named indexes {price}
# 2. numbered indexes {0},
# 3. or even empty placeholders {}.

# named indexes:
txt1 = "My name is {fname}, I'm {age}".format(
    age=36, fname="John")  # My name is John, I'm 36
# numbered indexes:
txt2 = "My name is {1}, I'm {0}".format(36, "John")  # My name is John, I'm 36
# empty placeholders:
txt3 = "My name is {}, I'm {}".format("John", 36)   # My name is John, I'm 36

print(txt1)
print(txt2)
print(txt3)

# :<    Left aligns the result (within the available space)
print("We have {:<8} chickens.".format(49))     # We have 49       chickens.

# :>    Right aligns the result (within the available space)
print("We have {:>8} chickens.".format(49))     # We have       49 chickens.

# :^    Center aligns the result (within the available space)
print("We have {:^8} chickens.".format(49))     # We have    49    chickens.

# :=    Places the sign to the left most position
# The temperature is       49 degrees celsius.
print("The temperature is {:=8} degrees celsius.".format(49))

# :+    Use a plus sign to indicate if the result is positive or negative
txt = "The temperature is between {:+} and {:+} degrees celsius."
print(txt.format(-3, 7))
# The temperature is between -3 and +7 degrees celsius.

# :-    Use a minus sign for negative values only
txt = "The temperature is between {:-} and {:-} degrees celsius."
print(txt.format(-3, 7))
# The temperature is between -3 and 7 degrees celsius.

# :     Use a space to insert an extra space before positive numbers (and a minus sign before negative numbers)
txt = "The temperature is between {:-} and {:} degrees celsius."
print(txt.format(-3, 7))
# The temperature is between -3 and 7 degrees celsius.

# :,    Use a comma as a thousand separator
txt = "The universe is {:,} years old."
print(txt.format(13800000000))
# The universe is 13,800,000,000 years old.

# :_    Use a underscore as a thousand separator
txt = "The universe is {:_} years old."
print(txt.format(13800000000))
# The universe is 13_800_000_000 years old.

# :b    Binary format
txt = "The binary version of {0} is {0:b}"
print(txt.format(5))
# The binary version of 5 is 101

# :c    Converts the value into the corresponding unicode character
# No sample

# :d    Decimal format
txt = "We have {:d} chickens."
print(txt.format(0b101))
# We have 5 chickens.

# :e    convert a number into scientific number format (with a lower-case e):
txt = "We have {:e} chickens."
print(txt.format(5))
# We have 5.000000e+00 chickens.

# :E    Scientific format, with an upper case E
txt = "We have {:E} chickens."
print(txt.format(5))
# We have 5.000000E+00 chickens.

# :f    Fix point number format
# default with 6 decimals
print("The price is {:f} dollars.".format(45))
# The price is 45.000000 dollars.

print("The price is {:.2f} dollars.".format(45))
# The price is 45.00 dollars.

# :F    Fix point number format, in uppercase format (show inf and nan as INF and NAN)
x = float('inf')

txt = "The price is {:F} dollars."
print(txt.format(x))    # The price is INF dollars.

txt = "The price is {:f} dollars."
print(txt.format(x))    # The price is inf dollars.


# :g    General format
# no sample

# :G    General format (using a upper case E for scientific notations)
# no sample

# :o    Octal format
txt = "The octal version of {0} is {0:o}"
print(txt.format(10))   # The octal version of 10 is 12

# :x    Hex format, lower case
txt = "The Hexadecimal version of {0} is {0:x}"
print(txt.format(255))  # The Hexadecimal version of 255 is ff

# :X    Hex format, upper case
txt = "The Hexadecimal version of {0} is {0:X}"
print(txt.format(255))
# The Hexadecimal version of 255 is FF

# :n    Number format
# no sampple

# :%  Percentage format
txt = "You scored {:%}"
print(txt.format(0.25))     # You scored 25.000000%

txt = "You scored {:.0%}"
print(txt.format(0.25))     # You scored 25%


print("\n--------index()--------\n")
# finds the first occurrence of the specified value.
# raises an exception if the value is not found.
#  is almost the same as the find() method, the only difference is that the find() method returns -1
#  if the value is not found.
# Parameter Description
# value     Required. The value to search for
# start     Optional. Where to start the search. Default is 0
# end       Optional. Where to end the search. Default is to the end of the string
print("Hello World",  "Hello World".index("o"))   # 4
print("Hello World",  "Hello World".index("o", 5))   # 7
print("Hello World",  "Hello World".index("o", 5, 8))   # 7
# print("Hello World",  "Hello World".index("o", 5, 7)) # 7     ValueError: substring not found
# print("Hello World",  "Hello World".index("o", 8))   # 7    ValueError: substring not found

txt = "Hello, welcome to my world."
print(txt.find("q"))        # -1
# print(txt.index("q"))       # ValueError: substring not found


print("\n--------isalnum()--------\n")
# True if all the characters are alphanumeric, meaning alphabet letter (a-z) and numbers (0-9).
print("Company 12".isalnum())   # false
print("Company12%".isalnum())   # false
print("Company12".isalnum())    # true
print("Company".isalnum())      # true
print("1233".isalnum())         # true
print("!$@##%^&".isalnum())     # false


print("\n--------isalpha()--------\n")
# True if all the characters are alphabet letters (a-z).
print("Company 12".isalpha())   # false
print("Company12%".isalpha())   # false
print("1233".isalpha())         # false
print("Company".isalpha())      # true


print("\n--------isdecimal()--------\n")
#  returns True if all the characters are decimals (0-9).
a = "\u0030"  # unicode for 0
b = "\u0047"  # unicode for G

print(a.isdecimal())        # True
print(b.isdecimal())        # False

print("Company".isdecimal())      # False
print("Company 12".isdecimal())   # false
print("Company12%".isdecimal())   # false
print("1233".isdecimal())         # True
