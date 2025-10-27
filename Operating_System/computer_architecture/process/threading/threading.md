# Computer Architecture - Process: Threading

[Back](../../index.md)

- [Computer Architecture - Process: Threading](#computer-architecture---process-threading)
  - [Thread](#thread)
  - [Multithreading](#multithreading)
  - [Lab: Single Thread vs Multithreading](#lab-single-thread-vs-multithreading)

---

## Thread

- `Processes` are heavy weight

  - each has comlete copy of code and memory.
  - communication is expensive, needing special coding
    - needs to wait IO, leading CPU idle.
  - make the `cpu time slicing` technique is not appropriate.
  - ideal for **CPU bound work**
    - perform computations in parallel

- `thread`
  - lightweight processes
    - run different code while waiting
  - operate inside the same process
    - Share memory
  - ideal for **IO bound concurrency**
    - one thread waiting for IO
    - another thread execute at the same time
  - no ideal for **CPU bound work**
    - slower than a process without multi-threading
    - due to the cost of swapping.

---

## Multithreading

2 common scheduling terms

- `preemptive multi-tasking`

  - **OS foces** relinquishment(交出或) of CPU

- `Cooperative multi-tasking`

  - the **program is in control** of swapping out

- `Green threads`
  - programming language has its own threading and multi-tasking machanism separate from the OS
  - Python `asyncio` library
    - a green thread library
    - cooperative multi-tasking
      - the code signals when it's ready to give up control, e.g., when it's waiting on some IO

---

## Lab: Single Thread vs Multithreading

```py
import time
import threading
import requests

# Simulate downloading a file (I/O-bound operation)


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


def single_threaded_downloads(urls):

    # get start time
    start_time = time.time()
    print("\n--- Starting Single-threaded Downloads ---")

    # batch download
    for i, url in enumerate(urls):
        download_file(url, f"file_single_threaded_{i+1}.json")

    # get end time
    end_time = time.time()

    print(
        f"Single-threaded downloads finished in {end_time - start_time:.2f} seconds")


def multithreaded_downloads(urls):

    # get start time
    start_time = time.time()
    print("\n--- Starting Multithreaded Downloads ---")

    # define treads
    threads = []
    for i, url in enumerate(urls):
        thread = threading.Thread(
            target=download_file,
            args=(
                url,
                f"file_multithreaded_{i+1}.json"
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
    end_time = time.time()
    print(
        f"Multithreaded downloads finished in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    FILE_URL = ["https://trip.arguswatcher.net/prod/trip-hour"] * 10

    single_threaded_downloads(FILE_URL)
    multithreaded_downloads(FILE_URL)

```

- Result:

```txt
--- Starting Single-threaded Downloads ---
Starting download of file_single_threaded_1.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_1.json
Starting download of file_single_threaded_2.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_2.json
Starting download of file_single_threaded_3.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_3.json
Starting download of file_single_threaded_4.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_4.json
Starting download of file_single_threaded_5.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_5.json
Starting download of file_single_threaded_6.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_6.json
Starting download of file_single_threaded_7.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_7.json
Starting download of file_single_threaded_8.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_8.json
Starting download of file_single_threaded_9.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_9.json
Starting download of file_single_threaded_10.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_single_threaded_10.json
Single-threaded downloads finished in 5.21 seconds

--- Starting Multithreaded Downloads ---
Starting download of file_multithreaded_1.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_2.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_3.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_4.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_5.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_6.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_7.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_8.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_9.json from https://trip.arguswatcher.net/prod/trip-hour
Starting download of file_multithreaded_10.json from https://trip.arguswatcher.net/prod/trip-hour
Finished download of file_multithreaded_2.json
Finished download of file_multithreaded_4.json
Finished download of file_multithreaded_8.json
Finished download of file_multithreaded_9.json
Finished download of file_multithreaded_3.json
Finished download of file_multithreaded_6.json
Finished download of file_multithreaded_7.json
Finished download of file_multithreaded_10.json
Finished download of file_multithreaded_5.json
Finished download of file_multithreaded_1.json
Multithreaded downloads finished in 0.77 seconds
```

- Takeaway

| Single Thread | Multithreading |
| ------------- | -------------- |
| `5.21s`       | `0.77s`        |
