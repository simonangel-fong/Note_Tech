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
