# R - Vector

[Back](../../index.md)

- [R - Vector](#r---vector)
  - [Vector](#vector)
    - [Create Vector](#create-vector)

---

## Vector

- `vector`:

  - a sequence of elements which share the same data type
  - supports logical, integer, double, character, complex, or raw data type.

- `components of the vector`:

  - The elements contained in vector

- Function to check the type of vector:

  - `typeof()`

- Classifications:
  - `Atomic vectors`: all the elements are of the same type
    - `Numeric vector`: contains numeric elements
    - `Integer vector`: contains integer elements
    - `Character vector`: contains character elements
    - `Logical vector`: contains Boolean values
  - `Lists`: the elements are of different data types.

---

### Create Vector

- In R, the last index is inclusive.

```r
# c() function
x<-c(10.1, 10.2, 33.2)
# 10.1 10.2 33.2
class(x)
# "numeric"

x<-c("shubham","arpita","nishka","vaishali")
class(x)
# "character"

# colon(:) operator
x<-1:10
#  1  2  3  4  5  6  7  8  9 10
x<-10:1
# 10  9  8  7  6  5  4  3  2  1


# seq() function
x<-seq(1,4,by=0.5)
# 1.0 1.5 2.0 2.5 3.0 3.5 4.0
class(x)  # "numeric"
```

---

[TOP](#r---vector)
