# Computer Architecture - Process: Race Condition

[Back](../../index.md)

- [Computer Architecture - Process: Race Condition](#computer-architecture---process-race-condition)
  - [Race condition](#race-condition)
  - [Race Condition Demo - ATM](#race-condition-demo---atm)
    - [Problem Demo](#problem-demo)
    - [Lock Solution Demo](#lock-solution-demo)

---

## Race condition

- `race condition`

  - a bug in a system when **multiple** `threads` access and modify `shared state` **without proper synchronization**, and the final result depends on the **unpredictable timing** (“who gets there first”) of those threads.
  - multiple thread executes the same code at the same time.

- `Critical section`

  - The smallest **block of code** that must not be executed by more than one thread at the same time because it touches shared, mutable state.
  - to make the **read–modify–write step atomic** (all-or-nothing) with respect to other threads.
  - Use a `synchronization primitive`to enforce mutual exclusion.
    - e.g., `threading.Lock`

- `Shared data`
  - Variables or objects that can be read/written **by multiple threads**.
  - Without synchronization, simultaneous access causes `race conditions` (**nondeterministic**, wrong results).

---

## Race Condition Demo - ATM

### Problem Demo

- Code: `race_condition.py`

```py
import threading
import time

balance = 2000


def withdraw(amount):
    # refering a global var
    global balance
    if amount <= balance:
        time.sleep(0.01)
        balance -= amount
        print(f"Withdrawn: {amount}")
    else:
        print("Invalid amount")


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
```

- result

```sh
Withdrawn: 1500
Withdrawn: 1500
Current balance: -1000
```

- explanation:

1. System check: An account has $2,000 and two people try to withdraw $1,500 each at the same time.
2. Thread 1 reads balance: The system checks the balance and sees $2,000, which is enough for the withdrawal.
3. Thread 2 reads balance: Before Thread 1 can update the balance, Thread 2 reads the same balance of $2,000.
4. Thread 1 updates balance: Thread 1 subtracts $1,500 and the balance becomes $500.
5. Thread 2 updates balance: Thread 2 also subtracts $1,500, bringing the balance to -$1,000, leaving the account overdrawn even though there was only enough money for one withdrawal.

---

### Lock Solution Demo

- Solution using lock

```py
import threading
import time

balance = 2000
# Create lock obj
lock = threading.Lock()

def withdraw(amount):
    # refering a global var
    global balance

    # acquire lock before Critical section
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
```

- result:

```sh
Withdrawn: 1500
Invalid amount
Current balance: 500
```

- Explanation

1. System check: An account has $2,000 and two people try to withdraw $1,500 each at the same time.
2. Thread 1 acquires lock, preventing Thread 2 execute the critical section.
3. Thread 1 reads balance: The system checks the balance and sees $2,000, which is enough for the withdrawal.
4. Thread 1 releases lock, allowing Thread 2 enter the critical section.
5. Thread 2 reads balance: Thread 2 reads the balance is 500.
6. Thread 2 finishes the execution with "Invalid amount"
7. Thread 2 releases lock.
