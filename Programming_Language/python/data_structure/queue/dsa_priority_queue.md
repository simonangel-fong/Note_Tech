# DSA - Priority Queue

[Back](../../index.md)

- [DSA - Priority Queue](#dsa---priority-queue)
  - [Priority Queue](#priority-queue)
  - [Implementation](#implementation)

---

## Priority Queue

- `priority queue`

  - a variation of a queue
  - items are **dequeued** by removing it **from the front**.

- Each element in a priority queue has **an associated priority**. In a priority queue, elements with high priority are served before elements with low priority.

  - The **highest priority items** are **at the front** of the queue and the **lowest priority** items are a**t the back**.
  - When enqueuing an item on a priority queue, the new item may move all the way to the front.

- Use Case:

---

## Implementation

- To improve performance, priority queues are typically based on a **heap**, giving `O(log n)` performance for **inserts** and **removals**, and `O(n)` to **build the heap** initially from a set of n elements.

- [Tree/Heap](../tree/dsa_heap.md)

---

[TOP](#dsa---priority-queue)
