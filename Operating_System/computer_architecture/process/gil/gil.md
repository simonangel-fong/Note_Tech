# Computer Architecture - Process: GIL

[Back](../../index.md)

- [Computer Architecture - Process: GIL](#computer-architecture---process-gil)
  - [Python GIL(Global Interpreter Lock)](#python-gilglobal-interpreter-lock)
    - [Asynchronious in FastAPI](#asynchronious-in-fastapi)
  - [Multipleprocesing vs Multiplethreading](#multipleprocesing-vs-multiplethreading)
  - [Lab: CPU-bound](#lab-cpu-bound)
  - [Lab: IO-bound](#lab-io-bound)

---

## Python GIL(Global Interpreter Lock)

- **Python is multithreaded for concurrency, but CPython isn’t multi-thread-parallel for pure Python CPU work in a single process.**

- `mutex(mutual exclusion lock)`

  - a synchronization primitive that **lets only one thread/task** enter a `critical section` at a time.
  - Everyone else trying to enter blocks (or spins) until the owner releases it.

- `mutext` in Python

  - `threading.Lock` — plain (non-reentrant) mutex.
  - `multiprocessing.Lock` — OS-level inter-process mutexes usable between processes
  - `asyncio.Lock` — a cooperative mutex for coroutines (no OS threads involved)

- `GIL(Global Interpreter Lock)`

  - a coordinator used to ensure two `threads` can't change the same value at the same time.
  - used to maintain the integrity of Python's memory management.
  - a **process-wide mutex** that lets only one OS thread execute Python bytecode at a time.

- Python `multiprocessing` effectively bypasses the `GIL`.

  - Python `threading.Thread` does not bypass the `GIL`.

- **Rule of thumb**:
  - **I/O-bound**: `threads` or `asyncio`.
  - **CPU-bound**: `multiprocessing`

---

### Asynchronious in FastAPI

- `async` in FastAPI

  - `async/await` = **cooperative concurrency** on a **single thread** via an event loop (usually uvloop/asyncio).
  - While one task waits (network, disk, sleep), the loop runs other tasks.
  - Great for I/O-bound apps (APIs, DB calls).

- `def` and `async def`:
  - `def`: executed in a threadpool so it won’t block the loop, but lose some `async` benefits.
  - `async def`: nonblocking if `await` async I/O.

---

## Multipleprocesing vs Multiplethreading

## Lab: CPU-bound

```py
import os
import time
from multiprocessing import Pool
import threading


def sum_of_squares(target: int) -> int:
    total = 0
    for i in range(target):
        total += i * i
    return total


def run_batch(task_list: list) -> list:

    # get start time
    start_time = time.perf_counter()
    print("\n---------- Running tasks in batch ----------")

    results = []
    for task in task_list:
        results.append(sum_of_squares(task))

    # get ending time
    end_time = time.perf_counter()
    print(f"Batch execution time: {end_time - start_time:.4f} seconds")
    return results


def run_multiprocessing(task_list: list, num_processes: int) -> list:

    # get starting time
    start_time = time.perf_counter()
    print("\n---------- Running tasks mutiprocessing ----------")

    # calculate the num processes
    procs = min(num_processes, os.cpu_count() or num_processes)
    # define process pool
    with Pool(processes=procs) as pool:
        results = pool.map(sum_of_squares, task_list)

    # get ending time
    end_time = time.perf_counter()

    print(
        f"Multiprocessing execution time ({procs} processes): {end_time - start_time:.4f} seconds")

    return results


def run_multithreading(task_list: list) -> list:

    # get starting time
    start_time = time.perf_counter()
    print("\n---------- Running tasks multithreading ----------")

    results = []

    # helping func
    def write_result(target: int):
        results.append(sum_of_squares(target))

    # define treads
    threads = []
    for i, target in enumerate(task_list):
        thread = threading.Thread(
            target=write_result,
            args=(target,)
        )
        threads.append(thread)

    # start threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # get end time
    end_time = time.perf_counter()
    print(
        f"Multithreading execution time: {end_time - start_time:.4f} seconds")

    return results


if __name__ == "__main__":
    TASK_VAL = 100_000_000
    TASK_NUM = 20

    tasks = [TASK_VAL] * TASK_NUM

    print(f"\nWorkload: {tasks}")

    batch_result = run_batch(task_list=tasks)
    # print(f"Result of batch: {batch_result}")

    multithreading_results = run_multithreading(task_list=tasks)
    # print(f"Result of multithreading: {multithreading_results}")

    multiprocessing_results = run_multiprocessing(
        task_list=tasks, num_processes=TASK_NUM)
    # print(f"Result of multiprocessing: {multiprocessing_results}")

```

- Result

```txt
Workload: [100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000]

---------- Running tasks in batch ----------
Batch execution time: 77.3435 seconds

---------- Running tasks multithreading ----------
Multithreading execution time: 82.5154 seconds

---------- Running tasks mutiprocessing ----------
Multiprocessing execution time (12 processes): 26.4278 seconds
```

- Takeaway:

| Batch     | Multithreading | Multiprocessing |
| --------- | -------------- | --------------- |
| `77.3435` | `82.5154`      | `26.4278`       |

- **Multithreading**

  - In CPython, `threads` **don’t speed up** CPU-bound code because of the `GIL`
  - only one thread executes Python bytecode at a time.
  - The thread creation, scheduling, and context-switch overhead make it a bit slower than the batch run.

- **Multiprocessing**: ≈2.25× faster than batch
  - Separate processes **bypass** the `GIL` and run truly **in parallel on multiple cores**.
  - The speedup isn’t 4× because of process start-up cost, inter-process coordination, cache/bandwidth contention, and Python loop overhead.

---

## Lab: IO-bound

```py
from multiprocessing import Pool
import os
import time
import threading
import requests


def download_file(url, filename):

    print(f"Starting download of {filename} from {url}")
    try:
        response = requests.get(url, stream=True)
        # Raise an exception for bad status codes
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Finished download of {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")


def download_batch(urls):

    # get start time
    start_time = time.perf_counter()
    print("\n---------- Starting Batch Downloads ----------")

    # batch download
    for i, url in enumerate(urls):
        download_file(url, f"file_batch_{i+1}.json")

    # get end time
    end_time = time.perf_counter()

    print(f"Batch downloads finished in {end_time - start_time:.2f} seconds")


def download_multithreading(urls):

    # get start time
    start_time = time.perf_counter()
    print("\n---------- Starting Multithreading Downloads ----------")

    # define treads
    threads = []
    for i, url in enumerate(urls):
        thread = threading.Thread(
            target=download_file,
            args=(
                url,
                f"file_multithreading_{i+1}.json"
            )
        )
        threads.append(thread)

    # start threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # get end time
    end_time = time.perf_counter()
    print(
        f"Multithreading downloads finished in {end_time - start_time:.2f} seconds")


def download_multiprocessing(urls: list, num_processes: int) -> None:

    # get starting time
    start_time = time.perf_counter()
    print("\n---------- Starting Multiprocessing Downloads ----------")

    # calculate the num processes
    procs = min(num_processes, os.cpu_count() or num_processes)

    task_list = [(url, f"file_multiprocessing_{i}.json")
                 for i, url in enumerate(urls)]

    # define process pool
    with Pool(processes=procs) as pool:
        pool.starmap(download_file, task_list)

    # get ending time
    end_time = time.perf_counter()

    print(
        f"Multiprocessing execution time ({procs} processes): {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    URL_NUM = 10
    URL_REMOTE = ["https://trip.arguswatcher.net/prod/trip-hour"]
    tasks = URL_REMOTE * URL_NUM

    print(f"Workload: {tasks}")

    download_batch(tasks)
    download_multithreading(tasks)
    download_multiprocessing(tasks, URL_NUM)

```

- Result

```txt

---------- Starting Batch Downloads ----------
Starting download of file_batch_1.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_1.json
Starting download of file_batch_2.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_2.json
Starting download of file_batch_3.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_3.json
Starting download of file_batch_4.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_4.json
Starting download of file_batch_5.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_5.json
Starting download of file_batch_6.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_6.json
Starting download of file_batch_7.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_7.json
Starting download of file_batch_8.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_8.json
Starting download of file_batch_9.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_9.json
Starting download of file_batch_10.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_batch_10.json
Batch downloads finished in 6.56 seconds

---------- Starting Multithreading Downloads ----------
Starting download of file_multithreading_1.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_2.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_3.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_4.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_5.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_6.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_7.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_8.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_9.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreading_10.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_multithreading_5.json
Finished download of file_multithreading_9.json
Finished download of file_multithreading_6.json
Finished download of file_multithreading_4.json
Finished download of file_multithreading_3.json
Finished download of file_multithreading_7.json
Finished download of file_multithreading_2.json
Finished download of file_multithreading_1.json
Finished download of file_multithreading_8.json
Finished download of file_multithreading_10.json
Multithreading downloads finished in 1.15 seconds

---------- Starting Multiprocessing Downloads ----------
Starting download of file_multiprocessing_0.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_1.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_2.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_3.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_4.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_5.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_6.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_7.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_8.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multiprocessing_9.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_multiprocessing_7.json
Finished download of file_multiprocessing_5.json
Finished download of file_multiprocessing_9.json
Finished download of file_multiprocessing_0.json
Finished download of file_multiprocessing_6.json
Finished download of file_multiprocessing_3.json
Finished download of file_multiprocessing_1.json
Finished download of file_multiprocessing_4.json
Finished download of file_multiprocessing_8.json
Finished download of file_multiprocessing_2.json
Multiprocessing execution time (10 processes): 1.57 seconds
```

- Takeaway:

| Batch  | Multithreading | Multiprocessing |
| ------ | -------------- | --------------- |
| `6.56` | `1.15`         | `1.57`          |

- **Batch**
  - One request at a time
  - Nothing overlaps.
- **Multithreading**
  - ~5–6× improvement over batch.
  - All 10 requests run concurrently in the same process.
  - For sockets, requests **releases** the `GIL` while waiting on the network, so `threads` can **overlap the waiting**.
- **Multiprocessing**
  - each worker is a separate process.
  - For I/O this brings no advantage over threads (the GIL isn’t the bottleneck) and **adds overhead**.
  - better than batch, but typically a bit slower than threads for I/O tasks.
- **Threads > processes**
  - The work is **dominated** by **network latency** and kernel I/O waits, not CPU. Threads overlap those waits with minimal overhead.
  - Processes add startup + IPC overhead without removing any I/O bottleneck (the GIL doesn’t matter for sockets).
