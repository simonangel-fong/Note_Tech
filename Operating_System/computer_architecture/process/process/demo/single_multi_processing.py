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

