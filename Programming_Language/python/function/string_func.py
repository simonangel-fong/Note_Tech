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


print("\n--------isdigit()--------\n")
# Returns True if all the characters are digits, otherwise False.
# Exponents, like ², are also considered to be a digit.


print("\u0030".isdigit())  # true, unicode for 0
print("\u00B2".isdigit())  # True, unicode for ²

print("Company 12".isdigit())   # False
print("Company".isdigit())      # False
print("1233".isdigit())         # True
print("12.33".isdigit())        # False


print("\n--------isidentifier()--------\n")
# Returns True if the string is a valid identifier, otherwise False.
# A string is considered a valid identifier if it only contains alphanumeric letters (a-z) and (0-9), or underscores (_). 
# A valid identifier cannot start with a number, or contain any spaces.
# 字符串能否符合命名规范

print("MyFolder".isidentifier())        # True
print("Demo002".isidentifier())         # True
print("2bring".isidentifier())          # False
print("my demo".isidentifier())         # False


print("\n--------islower()--------\n")
# returns True if all the characters are in lower case, otherwise False.
# Numbers, symbols and spaces are not checked, only alphabet characters.
print("Hello world!".islower())     # False
print("hello 123".islower())        # True
print("mynameisPeter".islower())    # False


print("\n--------isnumeric()--------\n")
# returns True if all the characters are numeric (0-9), otherwise False.
# Exponents, like ² and ¾ are also considered to be numeric values.
# "-1" and "1.5" are NOT considered numeric values, 
# because all the characters in the string must be numeric, and the - and the . are not.
print("Hello world!".isnumeric())     # False
print("\u0030".isnumeric())     # True, unicode for 0
print("\u00B2".isnumeric())     # True, unicode for &sup2
print("10km2".isnumeric())      # False
print("-1".isnumeric())         # False
print("1.5".isnumeric())        # False
print("1234".isnumeric())       # True


print("\n--------isprintable()--------\n")
# returns True if all the characters are printable, otherwise False.
print("Hello world!".isprintable())             # True
print("Hello! Are you #1?".isprintable())       # True
print("Hello!\nAre you #1?".isprintable())      # False


print("\n--------isspace()--------\n")
# returns True if all the characters in a string are whitespaces, otherwise False.
print("Helloworld!".isspace())      # False
print("Hello world!".isspace())     # False
print("   s   ".isspace())          # False
print("      ".isspace())           # True


print("\n--------istitle()--------\n")
# returns True if all words in a text start with a upper case letter, 
# AND the rest of the word are lower case letters, otherwise False.
# Symbols and numbers are ignored.
print("HELLO WORLD".istitle())                          # False
print("hello world".istitle())                          # False
print("Hello world".istitle())                          # False
print("Hello World".istitle())                          # True
print("123 Hello World".istitle())                      # True
print("Hello World %'!?".istitle())                     # True


print("\n--------isupper()--------\n")
# returns True if all the characters are in upper case, otherwise False.
# Numbers, symbols and spaces are not checked, only alphabet characters.
print("hello world".isupper())                          # False
print("Hello world".isupper())                          # False
print("Hello World".isupper())                          # False
print("HELLO WORLD".isupper())                          # True
print("HELLO WORLD 123".isupper())                      # True
print("HELLO WORLD %'!?".isupper())                     # True


print("\n--------join()--------\n")
# takes all items in an iterable and joins them into one string.
# A string must be specified as the separator.
# separator.join(iterable)
# Parameter iterable	Required. Any iterable object where all the returned values are strings

xSeparator = ","

xStr = "John"
result = xSeparator.join(xStr)
print(result)   # J,o,h,n

# set is not iterable, so get an error.
xSet = {"1","2","3"}
result = xSeparator.join(xSet)
print(result)   # 3,1,2 由于set是无序的,所以每次输出是

xList = ["1","2","3"]
result = xSeparator.join(xList)
print(result)   # 1,2,3

xDict = {"name": "John", "country": "Norway"}
xSeparator = "TT"
result = xSeparator.join(xDict)

print(result)   # nameTTcountry


print("\n--------ljust()--------\n")
# left align the string, using a specified character (space is default) as the fill character.
# Parameter	Description
# length	Required. The length of the returned string
# character	Optional. A character to fill the missing space (to the right of the string). Default is " " (space).
print("Hello".ljust(10),"|")            # Hello      |
print("Hello".ljust(10,"*"),"|")        # Hello***** |


print("\n--------lower()--------\n")
# returns a string where all characters are lower case.
print("HELLO WORLD".lower())                          # hello world
print("hello world".lower())                          # hello world
print("Hello World".lower())                          # hello world
print("123 Hello World".lower())                      # 123 hello world
print("Hello World %'!?".lower())                     # hello world %'!?


print("\n--------lstrip()--------\n")
# removes any leading characters (space is the default leading character to remove)
# Parameter	Description
# characters	Optional. A set of characters to remove as leading characters
print("        HELLO WORLD          ".lstrip(),"|")                             # HELLO WORLD           |
print(",,,,,ssaaww.....HELLO".lstrip(",.asw"),"|")                              # HELLO |


print("\n--------maketrans()--------\n")
# returns a mapping table that can be used with the translate() method to replace specified characters.
# returns a dictionary describing each replacement, in unicode.
# Parameter	Description
# x	        Required. If only one parameter is specified, this has to be a dictionary describing how to perform the replace. If two or more parameters are specified, this parameter has to be a string specifying the characters you want to replace.
# y	        Optional. A string with the same length as parameter x. Each character in the first parameter will be replaced with the corresponding character in this string.
# z	        Optional. A string describing which characters to remove from the original string.

txt = "Hi Sam!"
x = "mSa"
y = "eJo"

xtb = str.maketrans(x, y)
print(txt.translate(xtb))       # Hi Joe!

txt = "Good night Sam!"
x = "mSa"
y = "eJo"
z = "odnght"

xtb = str.maketrans(x, y, z)
print(xtb)
# {109: 101, 83: 74, 97: 111, 111: None, 100: None, 110: None, 103: None, 104: None, 116: None}    
print(txt.translate(xtb))           # G i Joe!


print("\n--------partition()--------\n")
# searches for a specified string, and splits the string into a tuple containing three elements.
# note: searches for the first occurrence of the specified string
#   The first element contains the part before the specified string.
#   The second element contains the specified string.
#   The third element contains the part after the string.
# If the specified value is not found, the partition() method returns a tuple containing: 
#   1 - the whole string, 
#   2 - an empty string, 
#   3 - an empty string
# Parameter	Description
# value	    Required. The string to search for
txt = "I could eat bananas all day"

xFound = txt.partition("bananas")
print(xFound)                    # ('I could eat ', 'bananas', ' all day')

xNotFound = txt.partition("apples")
print(xNotFound)                # ('I could eat bananas all day', '', '')


print("\n--------replace()--------\n")
# replaces a specified phrase with another specified phrase.
# All occurrences of the specified phrase will be replaced, if nothing else is specified.
# Parameter	Description
# oldvalue	Required. The string to search for
# newvalue	Required. The string to replace the old value with
# count	    Optional. A number specifying how many occurrences of the old value you want to replace. Default is all occurrences
txt = "one one was a race horse, two two was one too."

xReplace = txt.replace("one", "three")
print(xReplace)             # three three was a race horse, two two was three too.

xReplaceNotFound = txt.replace("xxx", "three")
print(xReplaceNotFound)        # one one was a race horse, two two was one too.

xReplaceCount = txt.replace("one", "three", 2)
print(xReplaceCount)        # three three was a race horse, two two was one too.


print("\n--------rfind()--------\n")
# finds the last occurrence of the specified value.
# returns -1 if the value is not found.
# Parameter	Description
# value	    Required. The value to search for
# start	    Optional. Where to start the search. Default is 0
# end	    Optional. Where to end the search. Default is to the end of the string
print("Hello World",  "Hello World".rfind(""))              # 11, the length of string
print("Hello World",  "Hello World".rfind("w"))             # -1
print("Hello World",  "Hello World".rfind("W"))             # 6
print("Hello World",  "Hello World".rfind("o"))             # 7
print("Hello World",  "Hello World".rfind("o", 7))          # 7 inclusive
print("Hello World",  "Hello World".rfind("o", 8))          # -1
print("Hello World",  "Hello World".rfind("o", 0, 7))       # 4 exclusive
print("Hello World",  "Hello World".rfind("o", 0, 8))       # 7


print("\n--------rindex()--------\n")
# finds the last occurrence of the specified value.
# raises an exception if the value is not found.
# Parameter	Description
# value	    Required. The value to search for
# start	    Optional. Where to start the search. Default is 0
# end	    Optional. Where to end the search. Default is to the end of the string
print("Hello World",  "Hello World".rindex(""))             # 11, the length of string
print("Hello World",  "Hello World".rindex("o"))            # 7
print("Hello World",  "Hello World".rindex("o", 7))         # 7, inclusive
# print("Hello World",  "Hello World".rindex("o", 8))       # ValueError: substring not found
print("Hello World",  "Hello World".rindex("o", 0, 7))      # 4, exclusive
# print("Hello World",  "Hello World".rindex("o", 0, 4))      # ValueError: substring not found


print("\n--------rjust()--------\n")
# right align the string, using a specified character (space is default) as the fill character.
# Parameter	Description
# length	Required. The length of the returned string
# character	Optional. A character to fill the missing space (to the left of the string). Default is " " (space).
print("Hello".rjust(10),"|")            #      Hello |
print("Hello".rjust(10,"*"),"|")        # *****Hello |
print("Hello world!".rjust(10,"*"),"|") # Hello world! |
# print("Hello".rjust(10,"*-"),"|")       # TypeError: The fill character must be exactly one character long


print("\n--------rpartition()--------\n")
# searches for the last occurrence of a specified string, and splits the string into a tuple containing three elements.
# note: 
#   The first element contains the part before the specified string.
#   The second element contains the specified string.
#   The third element contains the part after the string.
# If the specified value is not found, the rpartition() method returns a tuple containing: 
#   1 - an empty string, 
#   2 - an empty string, 
#   3 - the whole string:
# Parameter	Description
# value	    Required. The string to search for
txt = "I could eat bananas all day, bananas are my favorite fruit"
xFound = txt.rpartition("bananas")
print(xFound)       # ('I could eat bananas all day, ', 'bananas', ' are my favorite fruit')
xFound = txt.rpartition("apples")
print(xFound)       # ('', '', 'I could eat bananas all day, bananas are my favorite fruit')


print("\n--------split()--------\n")
# splits a string into a list.
# Parameter Description
# separator	Optional. Specifies the separator to use when splitting the string. By default any whitespace is a separator
# maxsplit	Optional. Specifies how many splits to do. Default value is -1, which is "all occurrences" When maxsplit is specified, the list will contain the specified number of elements plus one.
txt = "welcome to the jungle"
xList = txt.split()
print(xList)        # ['welcome', 'to', 'the', 'jungle']

txt = "hello, my name is Peter, I am 26 years old"
xList = txt.split(", ")
print(xList)        # ['hello', 'my name is Peter', 'I am 26 years old']

txt = "apple#banana#cherry#orange"
xList = txt.split("#")
print(xList)        # ['apple', 'banana', 'cherry', 'orange']

txt = "apple#banana#cherry#orange"
# setting the maxsplit parameter to 1, will return a list with 2 elements!
x = txt.split("#", -1)
print(x)            # ['apple', 'banana', 'cherry', 'orange']
x = txt.split("#", 0)
print(x)            # ['apple#banana#cherry#orange']
x = txt.split("#", 1)
print(x)            # ['apple', 'banana#cherry#orange']
x = txt.split("#", 2)
print(x)            # ['apple', 'banana', 'cherry#orange']
x = txt.split("#", 3)
print(x)            # ['apple', 'banana', 'cherry', 'orange']
x = txt.split("#", 4)
print(x)            # ['apple', 'banana', 'cherry', 'orange']


print("\n--------rsplit()--------\n")
# splits a string into a list, starting from the right.
# Parameter Description
# separator	Optional. Specifies the separator to use when splitting the string. By default any whitespace is a separator
# maxsplit	Optional. Specifies how many splits to do. Default value is -1, which is "all occurrences" When maxsplit is specified, the list will contain the specified number of elements plus one.
txt = "welcome to the jungle"
xList = txt.rsplit()
print(xList)        # ['welcome', 'to', 'the', 'jungle']

txt = "hello, my name is Peter, I am 26 years old"
xList = txt.rsplit(", ")
print(xList)        # ['hello', 'my name is Peter', 'I am 26 years old']

# txt = "apple#banana#cherry#orange"
# xList = txt.split("#")
# print(xList)        # ['apple', 'banana', 'cherry', 'orange']

txt = "apple#banana#cherry#orange"
# setting the maxsplit parameter to 1, will return a list with 2 elements!
x = txt.split("#", -1)
print(x)            # ['apple', 'banana', 'cherry', 'orange']
x = txt.rsplit("#", 0)
print(x)            # ['apple#banana#cherry#orange']
x = txt.rsplit("#", 1)
print(x)            # ['apple#banana#cherry', 'orange']
x = txt.rsplit("#", 2)
print(x)            # ['apple#banana', 'cherry', 'orange']
x = txt.rsplit("#", 3)
print(x)            # ['apple', 'banana', 'cherry', 'orange']
x = txt.rsplit("#", 4)
print(x)            # ['apple', 'banana', 'cherry', 'orange']


print("\n--------rstrip()--------\n")
# removes any trailing characters (characters at the end a string), space is the default trailing character to remove.
# Parameter	Description
# characters	Optional. A set of characters to remove as trailing characters
print("        HELLO WORLD          ".rstrip(),"|")     #         HELLO WORLD |
print(",,,,,ssaaww.....HELLO,,,,,ssaaww.....".rstrip(",.asw"),"|")      # ,,,,,ssaaww.....HELLO |


print("\n--------splitlines()--------\n")
# splits a string into a list. The splitting is done at line breaks.
# Parameter         Description
# keeplinebreaks	Optional. Specifies if the line breaks should be included (True), or not (False). Default value is False
print("Thank you for the music\nWelcome to the jungle".splitlines())        # ['Thank you for the music', 'Welcome to the jungle']
print("Thank you for the music\nWelcome to the jungle".splitlines(True))    # ['Thank you for the music\n', 'Welcome to the jungle']


print("\n--------startswith()--------\n")
# returns True if the string starts with the specified value, otherwise False.
# Parameter	Description
# value	    Required. The value to check if the string starts with
# start	    Optional. An Integer specifying at which position to start the search
# end	    Optional. An Integer specifying at which position to end the search
print("Hello, welcome to my world.".startswith("Hello"))                # True
print("Hello, welcome to my world.".startswith("wel", 7, 20))           # True


print("\n--------strip()--------\n")
# removes any leading (spaces at the beginning) and trailing (spaces at the end) characters (space is the default leading character to remove)
# Parameter 	Description
# characters	Optional. A set of characters to remove as leading/trailing characters
print("     banana     ".strip())       # banana
print(",,,,,rrttgg.....banana....rrr".strip(",.grt"))       # banana


print("\n--------swapcase()--------\n")
# returns a string where all the upper case letters are lower case and vice versa.
print("Hello My Name Is PETER".swapcase())      # hELLO mY nAME iS peter


print("\n--------title()--------\n")
# returns a string where the first character in every word is upper case. Like a header, or a title.
# If the word contains a number or a symbol, the first letter after that will be converted to upper case.
print("Welcome to my world".title())            # Welcome To My World
print("Welcome to my 2nd world".title())        # Welcome To My 2Nd World
print("hello b2b2b2 and 3g3g3g".title())        # Hello B2B2B2 And 3G3G3G


print("\n--------translate()--------\n")
# returns a string where some specified characters are replaced with the character described in a dictionary, or in a mapping table.
# Use the maketrans() method to create a mapping table.
# If a character is not specified in the dictionary/table, the character will not be replaced.
# If you use a dictionary, you must use ascii codes instead of characters.
# Parameter	Description
# table	    Required. Either a dictionary, or a mapping table describing how to perform the replace

xTable = str.maketrans("S", "P")
print("Hello Sam!".translate(xTable))       # Hello Pam!

xTable = str.maketrans("mSa", "eJo")
print("Hi Sam!".translate(xTable))          # Hi Joe! 

# The third parameter in the mapping table describes characters that you want to remove from the string
mytable = str.maketrans("mSa", "eJo", "odnght")
print("Good night Sam!".translate(mytable))     # G i Joe!

# When using a dictionary instead of a mapping table, must use ascii codes instead of characters.
xDict = {109: 101, 83: 74, 97: 111, 111: None, 100: None, 110: None, 103: None, 104: None, 116: None}
print("Good night Sam!".translate(xDict))       # G i Joe!


print("\n--------upper()--------\n")
# returns a string where all characters are in upper case.
# Symbols and Numbers are ignored.

print("Hello my friends".upper())       # HELLO MY FRIENDS
print("Hello World! (123)".upper())     # HELLO WORLD! (123)


print("\n--------zfill()--------\n")
# adds zeros (0) at the beginning of the string, until it reaches the specified length.
# If the value of the len parameter is less than the length of the string, no filling is done.
# Parameter	Description
# len	    Required. A number specifying the desired length of the string

print("50".zfill(10))                       # 0000000050
print("hello".zfill(10))                    # 00000hello
print("welcome to the jungle".zfill(10))    # welcome to the jungle
print("10.000".zfill(10))                   # 000010.000