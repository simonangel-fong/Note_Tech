# Python - Command Line Interface

[Back](../index.md)

- [Python - Command Line Interface](#python---command-line-interface)
  - [Command Line Interface](#command-line-interface)
  - [Example: CLI Calculator](#example-cli-calculator)
  - [Example: choices](#example-choices)

---

## Command Line Interface

- `command-line interface`, aka `CLI`:

  - interacts with a command-line script.

- `argparse` Library
  - Python `argparse` is a command-line parsing module that is recommended to work with the command line argument.

---

## Example: CLI Calculator

- `code.py`:

```py
# importing argparse module
import argparse
parser = argparse.ArgumentParser(
    desription="This program prints the result of two numbers"
)

# creating two variables using the add_argument method
parser.add_argument("num1", help = "first number")
parser.add_argument("num2", help = "second number")
parser.add_argument("operation", help = "operation")


args = parser.parse_args()

print(args.num1)
print(args.num2)
print(args.operation)

n1 = int(args.num1)
n2 = int(args.num2)


if args.operation == "add":
    result = n1 + n2
    print("The Result is : ",result)

elif args.operation == "sub":
    result = n1 - n2

elif args.operation == "mul":
    result = n1 * n2
elif args.operation == "div":
    result = n1 / n2
else:
    print("Unmatched Argument")

print("result is : ",result)
```

- `CLI`:

```shell
python code.py -h
# usage: code.py [-h] num1 num2 operation

# This program prints the result of two numbers

# positional arguments:
#   num1        first number
#   num2        second number
#   operation   operation

# optional arguments:
#   -h, --help  show this help message and exit

python code.py 33 33 add
# 33
# 33
# add
# The Result is :  66
# result is :  66

```

---

## Example: choices

- `cli_dog.py`

```py
import argparse

parser = argparse.ArgumentParser(
    description='This program prints the info of my dogs'
)

parser.add_argument(
    '-c',
    '--color',
    metavar='color',
    required=True,
    choices={'red', 'yellow'},
    help='the color to search for'
)

args = parser.parse_args()

print(args.color)

```

- CLI:

```shell
python cli_dog.py
# usage: cli_dog.py [-h] -c color
# cli_dog.py: error: the following arguments are required: -c/--color


python cli_dog.py -h
# usage: cli_dog.py [-h] -c color

# This program prints the info of my dogs

# optional arguments:
#   -h, --help                show this help message and exit
#   -c color, --color color   the color to search for


python cli_dog.py -c green
# usage: cli_dog.py [-h] -c color
# cli_dog.py: error: argument -c/--color: invalid choice: 'green' (choose from 'yellow', 'red')


python cli_dog.py -c red
# red

```

---

[TOP](#python---command-line-interface)
