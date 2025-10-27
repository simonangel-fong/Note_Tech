# Computer Architecture - Memory: Memory Segment

[Back](../../index.md)

- [Computer Architecture - Memory: Memory Segment](#computer-architecture---memory-memory-segment)
  - [Memory Segments](#memory-segments)
  - [Text/Code Segment](#textcode-segment)
  - [Data Segment](#data-segment)
  - [BSS(Block Started by Symbol) Segment](#bssblock-started-by-symbol-segment)
  - [Heap Segment](#heap-segment)
  - [Stack](#stack)
  - [OS Kernel Segment](#os-kernel-segment)

---

## Memory Segments

- `Memory Segments`

  - A process’s **virtual address space** is typically divided into **logical regions**, the `segments` with different purposes and permissions.

- A process is an instance of a program that requires CPU and memory.
  - Individual process cannot access the `physical memory` directly, but access the `virtual memory` mapping to `physical memory`.
- `Virtual memory` is divided into `pages` with same size; `Physical memory` is divided into `frames` with same size.
- The `virtual memory` of a `process` is divided into regions, each of which serves a specific purpose.

  - `Text/Code`
  - Data
  - BSS
  - heap
  - stack
  - operating system kernel space

- Benefits of memory segments
  - Security
    - Each memory region has specific access permissions and privilege level.
    - e.g.,
      - `Text/Code segment` is read only and executable.
      - `stack`, `heap` is readable and writable.
  - Access pattern (sequential vs random)
    - Each segment has different access pattern
    - e.g.,
      - `stack`: predictable sequential pattern making memory allocation easy and fast
      - `heap`: in dynamic and random memory allocation,
  - Isolation of bugs (buffer overflows)
    - prevent accidential overwrites and bugs like buffer overflow

---

## Text/Code Segment

- `text/code segment`
  - the memory segment contains executable instructions of the program, which typically is loaded from the binary file that contains compiled code.
  - permission:
    - read-only + executable (r-x)
    - prevent accidental/self-modifying writes.
  - segment size: = the required space to load the entire code.

---

## Data Segment

- `data segment`
  - the memory segment that store global/static variables that have initialized values(nonzero).
  - to reduce the size of executable files and make the file load faster
    - initialized variables needs to be explictly stored in the executable files when the program starts
  - permission
    - read/write (rw-).

---

## BSS(Block Started by Symbol) Segment

- `BSS(Block Started by Symbol) Segment`
  - the memory segment that store global/static variables that have uninitialized values(zero).
  - to reduce the size of executable files and make the file load faster
    - initialuninitializedized variables does not need to be stored in the executable files when the program starts
  - permission:
    - read/write (rw-).

---

## Heap Segment

- `heap`

  - the memory segment for dynamic allocation
  - e.g., `new` keyword in Java.
  - use the `memory allocator` to manage the memory available to the program **during runtime**.
  - Expands upward (to higher addresses) as request more memory.

- `memory allocator`:

  - tracks which part of memory are free and which are in use.
    - **finds** the suitable block of free memory, **marks** it as occupied, and hands over.
    - **reclaims** the block when the program is done.
  - it **takes time** to find free memory block and reclaim unused block, making **memory allocation and releases** in stack are **slow**.

- `memory leak`
  - a type of **programming error** where a program allocates memory but **fails to release it** after it's no longer needed.
  - **"leaked" memory** becomes **unusable** by other parts of the system and can accumulate over time,
    - leading to **performance degradation**, slow **response times**, and even application **crashes** as the system **runs out of available memory**.

---

## Stack

- `Stack`

  - the memory segment for simple and automatic storage
  - used to store temporary data,
    - local variables,
    - function parameters,
    - and return addresses during function calls.
  - structure:
    - `stack frame`
      - the more nested a function calls, the more frames are stacked on top
    - last in first out
  - Grows downward (to lower addresses)

- `stack pointer`

  - a small, special **register** in a computer's processor that holds the **memory address of the top/bottom** of the stack.
    - every time a `stack frame` is **pushed**, the `stack pointer` advances by the size of the frame.
    - When the frame is **popped**, the pointer moved back by the size of the last frame.
  - It is the reason why **memory allocation and releases** in stack are **fast**.

- `stack overflow`
  - an error that occurs when a program attempts to **store more data** on the stack than its **allocated capacity**
    - stack memory segment is limited to a certain size(1~8MB).
  - common cause:
    - a recursive function without a proper stopping condition
    - a function with a deep function call chain.
    - a function with unusually large local variables.
  - leading to a **program crash** or a segmentation fault.

---

## OS Kernel Segment

- `OS Kernel segment`
  - reserved for the OS pages, mapped to the OS systems kernel
