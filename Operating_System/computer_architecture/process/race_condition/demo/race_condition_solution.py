import threading
import time

balance = 2000
# Create lock obj
lock = threading.Lock()

def withdraw(amount):
    # refering a global var
    global balance

    # acquire lock before critical section
    lock.acquire()
    if amount <= balance:
        time.sleep(0.01)
        balance -= amount
        print(f"Withdrawn: {amount}")
    else:
        print("Invalid amount")
    
    # release lock when finish
    lock.release()


# thread object
atm1 = threading.Thread(
    target=withdraw,    # define function to call
    args=(1500,)     # define arguments for the function call
)

# thread object
atm2 = threading.Thread(
    target=withdraw,
    args=(1500,)
)

atm1.start()    # start execution of a thread
atm2.start()

atm1.join()     # block main thread until the thread object completes
atm2.join()

print(f"Current balance: {balance}")
