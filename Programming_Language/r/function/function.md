# R - Function

[Back](../index.md)

- [R - Function](#r---function)
  - [Function](#function)
  - [Conditions](#conditions)
    - [if-else](#if-else)
    - [for loop](#for-loop)
    - [while loop](#while-loop)
    - [repeat loop](#repeat-loop)
  - [Looping Functions](#looping-functions)
    - [lapply(): return a list](#lapply-return-a-list)
    - [sapply()](#sapply)
    - [tapply()](#tapply)
    - [apply()](#apply)
    - [mapply()](#mapply)
  - [`dplyr`](#dplyr)
    - [Installing and Loading Package](#installing-and-loading-package)
    - [filter()](#filter)
    - [arrange()](#arrange)
    - [slice()](#slice)
    - [select()](#select)
    - [rename()](#rename)
    - [mutate()](#mutate)
    - [summarise()](#summarise)

---

## Function

```r
function_name <- function(arg1, arg2, arg3, ...) {
    ## do any code in here when called
    return(return_object)
}

## Define a function that adds two numbers
add_numbers <- function(x, y) {
    return(x + y)
}
```

---

## Conditions

- Commonly used control structures are:
  - `if` and `else`: testing a condition and acting on it
  - `for`: execute a loop a fixed number of times
  - `while`: execute a loop **while a condition** is true
  - `repeat`: execute an **infinite loop** (must break out of it to stop)
  - `break`: break the execution of a loop
  - `next`: **skip** an iteration of a loop

---

### if-else

```r
if(condition){
    ## do any code here
}

if(condition){
    ## do any code here
}
else{
    ## do any code here
}

## Sequential stacking of if-else statements
if(condition){
    ## do any code here
}
else if(condition){
    ## do any code here
}
else{
    ## do any code here
}
```

---

### for loop

```r
for(loop_index in loop_vector) {
    ## do any code in here
}


for(i in c(1:5)) {
    print(i) ## Print the value of i
}
```

---

### while loop

```r
while(condition) {
    ## do any code in here
}

a=1
while(a <= 5) {
    print(a) ## Print the value of a
    a = a + 1 ## Increment the value of a
}
```

---

### repeat loop

```r
a=1
repeat {
    if(a == 5){
        break ## if the value of a is 5, terminate the loop
    }
    else {
        print(a)
        a = a+1
    }
}
```

---

## Looping Functions

- apply(): Apply a function over the margins of an array
- lapply(): Loop over a list and evaluate a function on each element
- sapply(): Same as lapply but try to simplify the result
- tapply(): Apply a function over subsets of a vector
- mapply(): Multivariate version of sapply

| Function   | Output Data Type | Description                                                                                                                                                 |
| ---------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `apply()`  | Array or Matrix  | Applies a function over the margins of an array (e.g., rows or columns). Works with arrays, matrices, and data frames.                                      |
| `lapply()` | List             | Applies a function to each element of a list and returns a list. Useful for operations on lists where the output length may vary.                           |
| `sapply()` | Depends on Input | Simplifies the output of `lapply()` into a vector or matrix. Attempts to simplify the result into the most meaningful data structure.                       |
| `tapply()` | Varies           | Applies a function over subsets of a vector, array, or data frame, grouped by a given factor or list of factors. Useful for applying a function by groups.  |
| `mapply()` | Depends on Input | Applies a function to the first elements of each argument, the second elements, and so on. Useful for element-wise operations on multiple vectors or lists. |

---

### lapply(): return a list

- lapply returns a list of the same length as X, each element of which is the result of applying FUN to the corresponding element of X

```r
x <- list(a = 1:10, beta = exp(-3:3), logic = c(TRUE,FALSE,FALSE,TRUE))
result <- lapply(x, mean) ## compute the list mean for each list element
result
# $a
# [1] 5.5

# $beta
# [1] 4.535125

# $logic
# [1] 0.5
class(result)
# [1] "list"
```

---

### sapply()

- sapply is a user-friendly wrapper of lapply
- simplifies the result into a vector or array
- The only difference is the returning output

```r
x <- list(a = 1:10, beta = exp(-3:3), logic = c(TRUE,FALSE,FALSE,TRUE))
result <- sapply(x, mean) ## compute the list mean for each list element
result
#        a     beta    logic
# 5.500000 4.535125 0.500000
class(result)
# [1] "numeric"
# "numeric" because all the elements in the result vector are numeric.
```

---

### tapply()

- Applies a specified function to subsets of a vector or data frame
- Useful for **splitting data into groups** based on a factor or a list of factors
- The function is **applied separately** to each group
- Returns a vector, array, or list, depending on the input data and the applied function

```r
groups <- as.factor(rbinom(32, n = 5, prob = 0.4))
groups
# [1] 9  11 13 17 13
# Levels: 9 11 13 17
tapply(groups, groups, length) ## is almost the same as table(groups)
#  9 11 13 17
#  1  1  2  1
table(groups)
# groups
#  9 11 13 17
#  1  1  2  1
```

---

### apply()

- apply takes a function and applies it to each **margin** of an array
- **Returns a vector or array or list** of values obtained by applying a function
  to margins of an array or matrix

```r
x <- matrix(1:12,nrow=4,ncol=3)
#      [,1] [,2] [,3]
# [1,]    1    5    9
# [2,]    2    6   10
# [3,]    3    7   11
# [4,]    4    8   12
apply(x, 1, sum) ## Take the mean of each row
# [1] 15 18 21 24
apply(x, 2, sum) ## Take the mean of each column
# [1] 10 26 42
```

---

### mapply()

- Applies a given function to **multiple input** vectors or lists element-wise.
- Useful for operations involving corresponding elements of multiple data structures.

```r
## Define a function that adds two numbers
add_numbers <- function(x, y) { return(x + y) }
# Create two vectors
vector1 <- c(1, 2, 3)
vector2 <- c(4, 5, 6)
# Apply the add_numbers function element-wise to the two vectors
result <- mapply(add_numbers, vector1, vector2)
# [1] 5 7 9
```

---

## `dplyr`

- dplyr is a powerful and popular **package for data manipulation** in R
- It is part of the "tidyverse" a collection of R packages designed for data science
- It provides a highly optimized set of routines specifically for dealing with data frames
- It provides a "grammar" for data manipulation and for operating on data frames
- Its functions are very fast, as many key operations are coded in **C++ **

---

- `filter()`: Used for **sub-setting** rows based on conditions
- `arrange()`: **Sorts** rows based on one or more variables
- `slice()`: **Chooses rows** based on location
- `select()`: **Picks specific columns** from a data frame
- `mutate()`: **Creates** new variables or **modifies** existing ones, new col
- `rename()`: **Rename** variables in a data framem, rename col
- `summarize()`: Generate summary statistics of different variables, it collapses a group into a single row
- `%>%: th`e “pipe” operator is used to connect multiple verb actions together into a pipeline

---

- Syntax

- The **first argument** is a `data frame`.
- The subsequent arguments describe **what to do with the data frame** specified in the first argument, and you can refer to **columns** in the data frame directly without using the `$` operator (just use the column names)
- The **return result** of a function is a new `data frame`
- Data frames must be properly formatted and annotated for this to all be useful. In particular, the data must be tidy52. In short, there should be one observation per row, and each column should represent a feature or characteristic of that observation

---

### Installing and Loading Package

```r
# Installing dplyr package
install.packages('dplyr', dependencies = T)

# Loading package
library('dplyr')
```

---

### filter()

- select a subset of rows in a data frame

```r
starwars %>% filter(skin_color == "light", eye_color == "brown")
```

---

### arrange()

- to reorder rows of a data frame according to one of the variables

```r
starwars %>% arrange(height) ## By default ascending sorting
starwars %>% arrange(desc(height)) ## desc is used for descending
starwars %>% arrange(height, mass) ## Sorting based on multiple columns
starwars %>% arrange(desc(height), mass)
```

---

### slice()

- to index rows by their (integer) locations. It allows you to select, remove, and duplicate rows

```r
starwars %>% slice(5:10)
starwars %>% slice_head(n=5) ## slice_head() and slice_tail() select the first or last rows
starwars %>% slice_random(n=5) ## slice_sample() randomly selects rows
starwars %>% filter(!is.na(height)) %>% slice_max(height, n=5) ## slice_min() and slice_max() select rows with highest or lowest values of a variable. We first must choose only the values which are not NA
```

---

### select()

- to select columns from a data frame

```r
# Select columns by name
starwars %>% select(hair_color, skin_color, eye_color)
# Select all columns between hair_color and eye_color (inclusive)
starwars %>% select(hair_color:eye_color)
# Select all columns except those from hair_color to eye_color (inclusive)
starwars %>% select(!(hair_color:eye_color))
# Select all columns ending with color.
starwars %>% select(ends_with("color"))
# Other choices are starts_with(), matches() and contains()
```

---

### rename()

- to change the name of a column in a Data Frame

```r
# Renaming a column from homeworld to home_world
starwars %>% rename(home_world = homeworld)
```

---

### mutate()

- Besides selecting sets of existing columns, it’s often useful to **add new columns** that are functions of existing columns
- mutate() is used to derive a new column based on an existing column in a Data Frame

```r
starwars %>% mutate(height_m = height / 100)
# If you only want to keep the new variables, use .keep = "none"
# We can’t see the height in meters we just calculated, but we can fix that using a select command
starwars %>%
    mutate(height_m = height / 100) %>%
    select(height_m, height, everything())
```

---

### summarise()

- summarise() is used to **aggregate data**. It collapses a data frame to a single row. It’s not that useful until we learn the `group_by()`

```r
starwars %>% summarise(height = mean(height, na.rm = TRUE))
# An example of using summarise with group_by()
starwars %>%
    group_by(species, sex) %>%
    select(height, mass) %>%
    summarise(
        height = mean(height, na.rm = TRUE),
        mass = mean(mass, na.rm = TRUE)
    )
```

---

[TOP](#r---function)
