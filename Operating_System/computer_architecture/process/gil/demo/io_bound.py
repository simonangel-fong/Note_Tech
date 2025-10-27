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
