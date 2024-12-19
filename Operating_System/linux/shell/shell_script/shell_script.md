# Linux - Shell: Script

[Back](../../index.md)

- [Linux - Shell: Script](#linux---shell-script)
  - [Shell Script](#shell-script)
  - [Key Concepts of Shell Scripting](#key-concepts-of-shell-scripting)
    - [Shebang (`#!`)](#shebang-)
    - [Basic Structure](#basic-structure)
    - [Make a Script Executable](#make-a-script-executable)
    - [Common Errors and](#common-errors-and)
  - [Variables](#variables)
    - [Single Quotes (') and Double Quotes (")](#single-quotes--and-double-quotes-)
    - [Parentheses `()` and Curly Braces `{}`](#parentheses--and-curly-braces-)
  - [Input/Output](#inputoutput)
    - [`read`: Read Input](#read-read-input)
    - [`echo`: Display message](#echo-display-message)
  - [Lab: Display OS information](#lab-display-os-information)
  - [Conditional Statements](#conditional-statements)
    - [`[[ ]]`](#-)
    - [Multiple Conditions](#multiple-conditions)
    - [Relational Operators](#relational-operators)
    - [String Comparison Operators](#string-comparison-operators)
    - [File Test Operators](#file-test-operators)
    - [`if-then`](#if-then)
    - [`If-Else`](#if-else)
    - [`elif`](#elif)
  - [Loops](#loops)
    - [Break and Continue](#break-and-continue)
    - [For Loop](#for-loop)
      - [Lab: List all username](#lab-list-all-username)
    - [C-Style for Loop](#c-style-for-loop)
    - [While Loop](#while-loop)
  - [Functions](#functions)
  - [Exit Codes](#exit-codes)
  - [Debugging](#debugging)
  - [Handle Errors Gracefully](#handle-errors-gracefully)

---

## Shell Script

- `Shell Script`
  - a **text file** containing a **series of commands** written for a shell (like Bash, Sh, or Zsh) to execute.
  - allows administrators and users to **automate** repetitive tasks, manage systems, and perform complex operations with ease.

---

## Key Concepts of Shell Scripting

### Shebang (`#!`)

- The **first line** of a shell script should **specify the interpreter to use**

```sh
#!/bin/bash
# use the bash shell to interpret the script.
```

---

### Basic Structure

- A shell script is essentially a **series of commands** executed in sequence
  - Shebang
  - comment
  - commands
  - statements

```sh
#!/bin/bash
# comments
echo "Hello, World!"
date
ls -l
```

---

### Make a Script Executable

- Make it executable with:

```sh
chmod +x myscript.sh
```

- Run the script:
  - Using the Relative or Absolute Path
  - Using the `bash` or `sh` Command
    - explicitly using bash or sh as interpreter
    - override the interpreter decleared in the shebang.
  - Using the Path Variable (`$PATH`)
    - execute the script without specifying its path, move it to a directory that is in your `$PATH`

```sh
# Using the Relative or Absolute Path
# absolute path
/absolute/path/myscript.sh

# relative path
./myscript.sh

# Using the `bash` or `sh` Command
bash /absolute/path/myscript.sh
sh /absolute/path/myscript.sh

bash ./myscript.sh
sh ./myscript.sh

# Using the Path Variable ($PATH)
mv hello.sh /usr/local/bin/
chmod +x /usr/local/bin/hello.sh
hello.sh  # execute the script without specifying its path
```

---

### Common Errors and

- "Permission Denied"
  - Solution: add x privilege

```sh
chmod +x hello.sh
```

- "Command Not Found"

  - Solution: Ensure you specify the correct path

- "Bad Interpreter: No Such File or Directory"
  - The shebang (#!) line may contain an incorrect interpreter path.

```sh
# Verify with:
which bash
```

---

## Variables

- `Variable`

  - Used to store data for reuse.

- Example:

```sh
#!/bin/bash
# Example of defining variables
a=Abc
b=XYZ
c="Linux class"

echo "My first name is $a"
echo "My surname is $b"
echo “My surname is $c”
```

---

### Single Quotes (') and Double Quotes (")

- **Single Quotes(`'`)**

  - The content inside single quotes is **treated exactly as it is written**.
  - Variables `($VAR)` and special characters like `\`, or `$` are **not expanded**.

- Exmaple of Single Quotes

```sh
touch single_quotes
chmod +x single_quotes

vi single_quotes
#!/bin/bash

VAR="Hello world"
echo 'Message: $VAR'
echo 'Message: ${VAR}'
echo 'Today is $(date)'
echo 'Today is `date`'

./single_quotes
# Message: $VAR
# Message: ${VAR}
# Today is $(date)
# Today is `date`
```

---

- **Double Quotes (`"`)**

  - Double quotes allow the shell to **expand variables** `($VAR)` and execute commands using **backticks** \`command\` or `$(command)`.
  - Double quotes **preserve spaces** and **special characters** as part of the string.

- Exmaple of Double Quotes

```sh
touch double_quotes
chmod +x double_quotes

vi double_quotes
# #!/bin/bash

# VAR="Hello world"
# echo "Message: $VAR"
# echo "Message: ${VAR}"
# echo "Today is $(date)"
# echo "Today is `date`"

./double_quotes
# Message: Hello world
# Message: Hello world
# Today is Tue Dec 17 18:43:02 EST 2024
# Today is Tue Dec 17 18:43:02 EST 2024
```

---

### Parentheses `()` and Curly Braces `{}`

- **Parentheses `()`**
  - **Subshell** Execution:
    - Commands enclosed within `()` are executed in a **subshell**, meaning any changes to the environment (e.g., variable values, directory changes) do not persist outside the subshell.
  - Command Grouping in Subshell
    - **group** multiple commands in parentheses, and they execute together in a subshell

```sh
touch parentheses
chmod +x parentheses

vi parentheses
# #!/bin/bash

# VAR="AAAA"
# ( VAR="BBBB"; echo "Inside subshell: $VAR" )
# echo "Outside subshell: $VAR"

./parentheses
# Inside subshell: BBBB
# Outside subshell: AAAA
```

---

- **Curly Braces `{}`**

  - Command Grouping **without Subshell**
    - Curly braces are used to group commands together, but without creating a subshell.
    - Changes made to the environment inside {} **persist outside** the group.
    - `{` and `}` must **have spaces** around them, and the commands must end with a **semicolon** (`;`) or a **newline**.
  - **Variable Expansion** with {}
    - Curly braces are used to clearly delineate variable names during expansion.

- example

```sh
touch braces
chmod +x braces

vi braces
# #!/bin/bash

# VAR="AAAA"
# { VAR="BBBB"; echo "Inside braces: $VAR"; }
# echo "Outside braces: $VAR"

./braces
# Inside braces: BBBB
# Outside braces: BBBB
```

---

- **Parentheses `()` vs Curly Braces `{}`**

```sh
touch ParenthesesBraces
chmod +x ParenthesesBraces

vi ParenthesesBraces
#!/bin/bash

VAR="Hello world"
echo "Message: $(VAR)"
echo "Message: ${VAR}"
echo "Message: $(date)"
echo "Message: ${date}"

./ParenthesesBraces
# ./ParenthesesBraces: line 4: VAR: command not found
# Message:
# Message: Hello world
# Message: Tue Dec 17 19:13:59 EST 2024
# Message:
```

---

## Input/Output

### `read`: Read Input

| CMD                           | DESC                                        |
| ----------------------------- | ------------------------------------------- |
| `read`                        | Read into default variable `REPLY`          |
| `read var_name`               | Read words into a variable                  |
| `read var1 var2`              | Read words into multiple variables          |
| `read -s password`            | Hides the input while typing.               |
| `read -p message -s password` | Display a prompt on the same line.          |
| `read -t 5`                   | Reading with a timeout in seconds.          |
| `read -r path`                | Prevent escape characterss                  |
| `read -a array_name`          | Reads input into an array                   |
| `read -n 1 array_name`        | Reads only a specified number of characters |

- Default Variable `$REPLY`

  - If no variable is specified, input is stored in the `REPLY` variable.

- By default, `read` interprets backslashes (`\`) as escape characters.

---

- Example: Multiple variables

```sh
read var1 var2
# input: AAA
echo $var1
# output: AAA
echo $var2
# output none

read var1 var2
# input: AAA BBB CCC
echo $var1
# output: AAA
echo $var2
# output: BBB CCC
```

- Example: Hides the input

```sh
read -p "Input login password:" -s password; echo
# Input login password:
echo $password
```

---

- Example of timeout

```sh
read -t 5 -p "Enter your name (5 seconds): " name
echo $name
```

---

- Example of Read into an arrays

```sh
read -a fruits -p "Enter three fruits:"
# input: Apple Orange Banana
echo "First: ${fruits[0]}, Second: ${fruits[1]}, Third: ${fruits[2]}"
# First: Apple, Second: Orange, Third: Banana
```

---

- Example of read a character

```sh
read -n 1 -p "Press [A] for option A. Any other key to exit:" key; echo
echo "Your key: $key"
```

---

- **Output**
  - using `echo` command
    - `echo`: Output a newline
    - `echo message`: Output a text message
    - `echo $var_name`: Output a variable

```sh
touch read_input
chmod +x read_input

vi read_input
#!/bin/bash
echo "Enter your name:"
read NAME
echo "Hello, $NAME!"

./read_input
```

---

### `echo`: Display message

| CMD                                      | DESC                          |
| ---------------------------------------- | ----------------------------- |
| `echo`                                   | Display a newline             |
| `echo "A text message"`                  | Display a message             |
| `echo "Hello, $name!"`                   | Display with variable value   |
| `echo "Today is $(date)"`                | Display with command          |
| `echo -n "This is a single line"`        | Suppress newline              |
| `echo -e "Line 1\nLine 2\tIndented"`     | Enable Escape Characters      |
| `echo -e "\e[31mThis is red text.\e[0m"` | Print colored text            |
| `echo "This is a log entry." > log.txt`  | Overwrites the file.          |
| `echo "This is a log entry." >> log.txt` | Append to the end of the file |

- By default, echo appends a newline (`\n`) **at the end** of its output.
- By default, escape sequences are ignored.

- Colors:

| Code | Color           |
| ---- | --------------- |
| `31` | Red             |
| `32` | Green           |
| `33` | Yellow          |
| `34` | Blue            |
| `35` | Magenta         |
| `36` | Cyan            |
| `0m` | Reset (default) |

---

- Redirect Output:

```sh
ls > output.txt   # Save output to a file
cat < input.txt   # Use file content as input
```

---

## Lab: Display OS information

```sh
#!/bin/bash
host=`hostname`
echo -e "Hostname: \e[32m$host\e[0m"
echo -e "Current user: \e[32m$(whoami)\e[0m"
echo -e "Current direcotry: \e[32m$(pwd)\e[0m"

```

---

## Conditional Statements

### `[[ ]]`

- `[[ ]]`

  - an enhanced test command that supports additional features like:
    - Logical operators: `&&` (AND), `||` (OR).
    - Pattern matching.

- Syntax:

```sh
name="Alice"

if [[ $name == A* && $name != "Admin" ]]
then
    echo "Hello, $name!"
fi
```

---

### Multiple Conditions

1. `AND` Condition

```sh
if [ $num -gt 5 ] && [ $num -lt 15 ]
then
    echo "The number is between 5 and 15."
fi
```

2. `OR` Condition

```sh
if [ $num -lt 5 ] || [ $num -gt 15 ]
then
    echo "The number is outside the range of 5 to 15."
fi
```

---

### Relational Operators

| Operator | Description              |
| -------- | ------------------------ |
| `-eq`    | Equal to                 |
| `-ne`    | Not equal to             |
| `-gt`    | Greater than             |
| `-ge`    | Greater than or equal to |
| `-lt`    | Less than                |
| `-le`    | Less than or equal to    |

---

### String Comparison Operators

| Operator | Description                     |
| -------- | ------------------------------- |
| `==`     | Equal to                        |
| `!=`     | Not equal to                    |
| `-z`     | True if the string is empty     |
| `-n`     | True if the string is not empty |

---

### File Test Operators

| Operator | Description            |
| -------- | ---------------------- |
| `-e`     | File exists            |
| `-f`     | File is a regular file |
| `-d`     | File is a directory    |
| `-r`     | File is readable       |
| `-w`     | File is writable       |
| `-x`     | File is executable     |

---

### `if-then`

- `if-then`

  - used for conditional execution of code.
  - It allows you to test a condition and execute a block of commands only if the condition is true.

- Syntax:

```sh
if [ condition ]
then
    commands
fi
```

---

### `If-Else`

- Syntax:

```sh
if [ condition ]
then
    commands_if_true
else
    commands_if_false
fi
```

---

### `elif`

- `elif` (else if) clause:

  - allows to test multiple conditions.

- Syntax:

```sh
if [ condition1 ]
then
    commands_if_condition1_true
elif [ condition2 ]
then
    commands_if_condition2_true
else
    commands_if_all_false
fi
```

---

## Loops

### Break and Continue

- `break`:
  - Exits the loop entirely.

```sh
for num in 1 2 3 4 5
do
  if [ $num -eq 3 ]
  then
    break
  fi
  echo "Number: $num"
done
# Number: 1
# Number: 2
```

---

- `continue`:
  - Skips the current iteration and moves to the next one.

```sh
for num in 1 2 3 4 5
do
  if [ $num -eq 3 ]
  then
    continue
  fi
  echo "Number: $num"
done
# Number: 1
# Number: 2
# Number: 4
# Number: 5
```

---

### For Loop

- `for-loop` statement
  - used to iterate over a series of items (like strings, numbers, files, etc.) or execute commands repeatedly for a defined number of times.
  - It simplifies repetitive tasks and is one of the fundamental looping constructs in shell scripting.

---

- **Iterating Over a List of Items**

- Syntax

```sh
for item in list
do
    commands
done
```

- Example

```sh
# Example: Iterating Over a List
for fruit in apple banana cherry
do
    echo "I like $fruit."
done
# I like apple.
# I like banana.
# I like cherry.

# Example: Iterating Over a Range of Numbers
for num in {1..5}
do
    echo "Number: $num"
done
# Number: 1
# Number: 2
# Number: 3
# Number: 4
# Number: 5

# Example: Looping Through Files
for file in *.txt
do
    echo "Processing file: $file"
done
# Processing file: a.txt
# Processing file: b.txt
# Processing file: c.txt
# Processing file: d.txt


# Example: Using Command Substitution
for user in $(cat users.txt)
do
    echo "Welcome, $user!"
done
# Welcome, AA!
# Welcome, BB!
# Welcome, CC!
# Welcome, ZZ!

for dir in $(ls /home)
do
    echo "Directory: $dir"
done
# Directory: rheladmin
# Directory: serveradmin

# Nested for Loops
for i in 1 2 3
do
    for j in A B
    do
        echo "Combination: $i$j"
    done
done
# Combination: 1A
# Combination: 1B
# Combination: 2A
# Combination: 2B
# Combination: 3A
# Combination: 3B

```

---

#### Lab: List all username

```sh
#!/bin/bash
i=1
for username in `awk -F: '{print $1}' /etc/passwd`
do
  echo "Username $((i++)) : $username"
done
```

---

### C-Style for Loop

- Syntax

```sh
for (( initialization; condition; increment ))
do
    commands
done
```

- Example

```sh
for (( i=1; i<=5; i++ ))
do
    echo "Iteration: $i"
done
# Iteration: 1
# Iteration: 2
# Iteration: 3
# Iteration: 4
# Iteration: 5
```

---

### While Loop

- `while loop`

  - used to execute a block of commands repeatedly as long as a specified condition is true.

- Syntax

```sh
while [ condition ]
do
    commands
done
```

---

- Example

```sh
# Simple Counter
#!/bin/bash
count=1
while [ $count -le 5 ]
do
  echo "Count: $count"
  count=$((count + 1))
done
# Count: 1
# Count: 2
# Count: 3
# Count: 4
# Count: 5

# Infinite Loop
#!/bin/bash
while true
do
    echo "This is an infinite loop. Press Ctrl+C to stop."
    sleep 1
done

# Command Output as a Condition
#!/bin/bash
while ping -c 1 google.com > /dev/null
do
    echo "Internet is up."
    sleep 5
done
echo "Internet is down."
```

---

## Functions

- Define reusable blocks of code

```sh
greet() {
  echo "Hello, $1!"
}
greet "User"
```

---

## Exit Codes

- Every command in a shell script returns an exit code:
  - `0` for **success**.
  - `Non-zero` for **failure**.
- Check the exit code using `$?`

```sh
mkdir test_dir
if [ $? -eq 0 ]; then
  echo "Directory created successfully."
else
  echo "Failed to create directory."
fi
```

---

## Debugging

- Run a script in debug mode to troubleshoot:

```sh
bash -x script.sh
```

---

## Handle Errors Gracefully

- Use exit codes and error messages.

```sh
if [ $? -ne 0 ]; then
  echo "Error occurred!"
  exit 1
fi
```
