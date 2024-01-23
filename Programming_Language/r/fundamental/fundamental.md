# R - Fun

[Back](../index.md)

- [R - Fun](#r---fun)
  - [Help in R](#help-in-r)
  - [Basic Math in R](#basic-math-in-r)
    - [Assigning Objects](#assigning-objects)
  - [Data Structures in R](#data-structures-in-r)
    - [Vectors](#vectors)
    - [Lists](#lists)
    - [Matrix](#matrix)
    - [Arrays](#arrays)
    - [Data Frames](#data-frames)
    - [Factors](#factors)

---

- Features

  - Software that provides programming environment for Statistical Data Analysis
  - Based on S
  - Interpreted Language
  - Data Storage, Analysis, Graphing
  - Free and Open-Source Software

- Strengths

  - Free and Open Source
  - Strong User Community
  - Highly extensible, flexible
  - Implementation of high-end statistical methods
  - Flexible graphics and intelligent defaults

- Weakness

  - Steep learning curve
  - Slow for large datasets

- Fundamental

  - Highly Functional
    - Everything done through functions
    - Strict named arguments
    - Abbreviations in arguments OK (e.g. T for TRUE)
  - Object Oriented
    - Everything is an object
    - “<-” is an assignment operator
    - “X <- 5”: X GETS the value 5

- Programming in R

  - Functions & Operators typically work on entire vectors
  - Expressions surrounded by {}
  - Codes separated by newlines, “;” not necessary
  - You can write your own functions and use them

- Descriptive Statistics

  - Has functions for all common statistics
  - summary() gives lowest, mean, median, first, third quartiles, highest for numeric variables
  - stem() gives stem-leaf plots
  - table() gives tabulation of categorical variables

- Statistical Modeling
  - Numerous libraries & packages
  - Distinction between factors and regressors
    - factors: categorical, regressors: continuous
    - you must specify factors unless they are obvious to R
    - dummy variables for factors created automatically
  - Use of data.frame makes life easy

---

## Help in R

- From Documentation:
  - ?WhatIWantToKnow
  - help(“WhatIWantToKnow”)
  - help.search(“WhatIWantToKnow”)
  - help.start()
  - getAnywhere(“WhatIWantToKnow”)
  - example(“WhatIWantToKnow”)
- Documents: “Introduction to R”
- Active Mailing List
  - Archives
  - Directly Asking Questions on the List

---

## Basic Math in R

- When you input a mathematical expression in the R console, it functions as a calculator
- Common arithmetic operations and mathematical functionality are available at the console prompt
- Addition, subtraction, multiplication and division can be performed with the +, -, \* and / symbols respectively
- Exponents (powers or indices) can be performed using ^.
- The order of calculations in a single command can be controlled with parentheses ()
- Square root, logarithms and exponents can be performed with the sqrt(), log() and exp() functions respectively

---

### Assigning Objects

- In R, assignment can be specified in two ways:
  - Using arrow notation (`<-`)
  - Using a single equal sign (`=`).

---

## Data Structures in R

- Supports virtually any type of data
- Numbers, characters, logicals (TRUE/ FALSE)
- Arrays of virtually unlimited sizes
- Simplest: `Vectors` and `matrices`
- `Lists`: Can contain **mixed** type variables
- `Data Frame`: Rectangular/Tabular dataset

|               | Linear  | Rectangular |
| ------------- | ------- | ----------- |
| All Same Type | Vectors | Matrix      |
| Mixed         | List    | Data Frame  |

- built-in data types
  - Atomic classes: numeric, logical, character, integer, complex vectors, lists
  - Factors
  - Data frames and matrices

---

### Vectors

- Essential building block for handling multiple items in R.
- Homogeneous data structures.
- Can be numeric, character, logical, etc.
- Created using `c()` function.

- Example:

```r
my.vector <- c(1.5, 2.9, 3.0)
my.vector[5:8]

len(my.vector)
class(my.vector)
sort(my.vector, decreasing = TRUE)
rep(x=10, times = 5) ## Repeat 10, 5 times
seq(from=3,to=27,by=3)
## Returns a vector of values from 3 to 27 with interval of 3.

# Explicit Coercion
my.vector <- c(1.5, 2.9, 3.0)
as.numeric(my.vector) ## Numeric
as.character(my.vector) ## Character

# Implicit Coercion
my.vector <- c(1.5, "a") ## Character
my.vector <- c(2, TRUE) ## Numeric
my.vector <- c(TRUE, "a") ## Character
```

---

### Lists

- Lists are highly valuable data structures in R
- **Heterogeneous** data structures
- Can contain elements of **different data types**
- A single list can contain diverse elements such as a numeric matrix, a logical array, a character string, and a factor object.
- Created using `list()` function

```r
my.list <- list(matrix(data=1:4,nrow=2,ncol=2), c(F,F,T,T),"Hello World")
# [[1]]
#      [,1] [,2]
# [1,]    1    3
# [2,]    2    4

# [[2]]
# [1] FALSE FALSE  TRUE  TRUE

# [[3]]
# [1] "Hello World"

my.list <- vector("list", length = 5) ## Create an empty list of a pre-specified length
# [[1]]
# NULL

# [[2]]
# NULL

# [[3]]
# NULL

# [[4]]
# NULL

# [[5]]
# NULL
my.list[[1]] ## Read data from index 1. Indexes are entered in double square brackets.
# NULL

length(my.list) ## To find out the length of a list
# 5
```

---

### Matrix

- `Matrix` is simply **several vectors** stored together
- **Two-dimensional** data structures
- Elements are of the **same data type**
- The size of a matrix is specified by number of rows and number of columns.
- Created using `matrix()` function

- Example:

```R
my.matrix <- matrix(c(1,2,3,4,5,6,7,8,9), nrow = 3, ncol = 3)
my.matrix <- matrix(c(1,2,3,4,5,6,7,8,9), nrow = 3, ncol = 3, byrow = FALSE)
## It will fill data column-wise fashion 先沿着col, 再row
#      [,1] [,2] [,3]
# [1,]    1    4    7
# [2,]    2    5    8
# [3,]    3    6    9
my.matrix <- matrix(c(1,2,3,4,5,6,7,8,9), nrow = 3, ncol = 3, byrow = TRUE)
## It will fill data row-wise fashion. 先沿着row, 再col
#      [,1] [,2] [,3]
# [1,]    1    2    3
# [2,]    4    5    6
# [3,]    7    8    9

dim(my.matrix) ## Returns the size of a matrix
# [1] 3 3

# Vector to matrix directly by adding dimension attribute
my.vector <- c(1,2,3,4,5,6,7,8,9)
dim(my.vector) <- c(3,3) ##
#      [,1] [,2] [,3]
# [1,]    1    4    7
# [2,]    2    5    8
# [3,]    3    6    9


my.matrix <- rbind(c(1:3), c(4:6)) ## binds data row-wise fashion
my.matrix
#      [,1] [,2] [,3]
# [1,]    1    2    3
# [2,]    4    5    6

my.matrix <- cbind(c(1,4), c(2,5), c(3,6)) ## binds data column-wise fashion
my.matrix
#      [,1] [,2] [,3]
# [1,]    1    2    3
# [2,]    4    5    6
```

---

### Arrays

- Multi-dimensional generalization of vectors
- Can have more than two dimensions
- Created using `array()` function

```r
my.array <- array(data=1:24,dim=c(3,4,2))
## Each of the two layers constitutes a 3 × 4 matrix as shown in the diagram
# 3 × 4 × 2 array: y * x * z

dim(my.array)
# [1] 3 4 2

my.array[1,2, 1] ## Reads element of first row and second column from 1st layer
my.array[,,2] ## Read all rows and all columns from 2nd layer
my.array[,2,] ## Read second column from both layers
my.array[2, c(1,3), 1] ## Read second row and specific columns (1 and 3) from 1st layer
my.array[2, c(-2,-4), 1] ## Read second row by omitting columns 2 and 4 from 1st layer
my.array[2, 2, 1] <- 32 ## Overwrites the value of second row and second column in 1st layer
my.array[, , -1] ## Read all rows and all columns from by omitting 1st layer
```

---

### Data Frames

- Data frames are used to store **tabular data** in R
- **Rectangular data** structures with rows and columns
- Columns can be of **different data types**
- Created using `data.frame()` function
- It can store numeric data, factor data, and so on

```r
my.dataframe <- data.frame(
    person=c("Peter","Lois","Meg","Chris", "Stewie"),
    age=c(42,40,17,14,1),
    sex=factor(c("M","F","F","M","M"))
    )
## A data frame with the first name, age in years, and sex of five individuals.
#   person age sex
# 1  Peter  42   M
# 2   Lois  40   F
# 3    Meg  17   F
# 4  Chris  14   M
# 5 Stewie   1   M

length(my.dataframe) ## It will return the size of a data frame
# 3

my.dataframe[1,2] ## Reads element of first row and second column
my.dataframe[, c(1,3)] ## Read all rows and specific columns (1 and 3)
my.dataframe[, c(-3)] ## Read all rows by omitting columns 2
my.dataframe$person ## Reading data by using the names of the vectors
my.dataframe[my.dataframe$age>17,] ## Filters data where age is greater than 17 newrecord <- data.frame(person="Brian",age=7, sex=factor("M"))
my.dataframe <- rbind(my.dataframe,newrecord) ## Add a new row by using rbind
funny <- c("High","High","Low","Med","High","Med")
my.dataframe <- cbind(my.dataframe,funny) ## Add a new variable by using cbind
```

---

### Factors

- Used to represent categorical data
- Can have levels indicating categories
- Useful for ordinal variables
- Created using `factor()` function

```r
funny <- c("High","High","Low","Med","High","Med")
my.factor <- factor(x=funny, levels=c("Low","Med","High"))
# [1] High High Low  Med  High Med
# Levels: Low Med High
```

