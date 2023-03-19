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
