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
