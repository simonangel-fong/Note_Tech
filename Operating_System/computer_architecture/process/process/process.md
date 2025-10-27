# Computer Architecture - Process

[Back](../../index.md)

- [Computer Architecture - Process](#computer-architecture---process)
  - [Process](#process)
  - [Multiprocessing](#multiprocessing)
  - [Lab: Single Process vs Multiprocessing](#lab-single-process-vs-multiprocessing)

---

## Process

- `process`

  - a logical grouping of
    - **execution code**
    - **system resources**
      - permissions
      - memory:
        - stack: used to track what functions have been called
        - heap: general purpose memory

- OS process models control which process is in charge of a CPU at any given time.
- `cpu time slice`
  - a technique in operating systems where a small, fixed **interval of CPU time**, called a "time slice" or "quantum," is **allocated to each active `process` or `thread`**.
  - swap multiple program and user's code in and out

---

## Multiprocessing

- `Multiple processes`

  - allow a program to spawn **separate processes**.
  - each process gets its own copy of code and memory.

- `Trivial concurrency(微不足道的并发)`

  - each process can do its own thing and require no information from the other processes.

- `inter-process communication`
  - a mechenism provided by the OS for two processes to exchange data.

---

## Lab: Single Process vs Multiprocessing

```py
import time
from multiprocessing import Pool

# A CPU-bound task: calculating the sum of squares for a range of numbers


def sum_of_squares(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_single_processing(numbers):

    # get starting time
    start_time = time.time()
    print("Running tasks serially:")

    # define and execute batch task
    results = []
    for num in numbers:
        results.append(sum_of_squares(num))

    # get ending time
    end_time = time.time()

    print(f"Single processing execution time: {end_time - start_time:.4f} seconds")
    return results


def run_multiprocessing(numbers, num_processes):

    # get starting time
    start_time = time.time()
    print("\nRunning tasks with multiprocessing:")

    # define process pool
    with Pool(processes=num_processes) as pool:
        results = pool.map(sum_of_squares, numbers)

    # get ending time
    end_time = time.time()

    print(
        f"Multiprocessing execution time ({num_processes} processes): {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    LOW_VAL = 1_000_000
    HIGH_VAL = 100_000_000
    NUM_TASK = 4

    low_tasks = [LOW_VAL] * NUM_TASK
    high_tasks = [HIGH_VAL] * NUM_TASK

    print(f"\nExecute low workload: {low_tasks}")
    singleprocessing_results = run_single_processing(low_tasks)
    multiprocessing_results = run_multiprocessing(low_tasks, NUM_TASK)


    print(f"\nExecute high workload: {high_tasks}")
    singleprocessing_results = run_single_processing(high_tasks)
    multiprocessing_results = run_multiprocessing(high_tasks, NUM_TASK)
```

- Result

```txt
Execute low workload: [1000000, 1000000, 1000000, 1000000]
Running tasks serially:
Single processing execution time: 0.1137 seconds

Running tasks with multiprocessing:
Multiprocessing execution time (4 processes): 0.2128 seconds

Execute high workload: [100000000, 100000000, 100000000, 100000000]
Running tasks serially:
Single processing execution time: 13.6597 seconds

Running tasks with multiprocessing:
Multiprocessing execution time (4 processes): 7.4814 seconds
```

- Takeaway:

| Workload                    | Single Processing | Multiprocessing |
| --------------------------- | ----------------- | --------------- |
| Low workload (1,000,000)    | `0.1137s`         | `0.2128s`       |
| High workload (100,000,000) | `13.6597s`        | `7.4814s`       |
