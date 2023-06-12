# Data Structure - Linked List

[Back](../index.md)

---

- [Data Structure - Linked List](#data-structure---linked-list)
  - [Linked List](#linked-list)
  - [Singly \& Doubly Linked Lists](#singly--doubly-linked-lists)
  - [Pros and Cons](#pros-and-cons)
  - [Complexity](#complexity)

---

## Linked List

- `Linked List`:

  - a sequential list of nodes that hold data which point to other nodes also containing data.

- Usage:

  - Used in many List, Queue & Stack implementations.
  - Great for creating circular lists.
  - Can easily model real world objects such as trains.
  - Used in separate chaining, which is present certain Hashtable implementations to deal with hashing collisions.
  - Often used in the implementation of adjacency lists for graphs.

- Terminology
  - `Head`: The first node in a linked list
  - `Tail`: The last node in a linked list
  - `Pointer`: Reference to another node
  - `Node`: An object containing data and pointer(s)

---

## Singly & Doubly Linked Lists

- `Singly Linked Lists`:

  - only hold a reference to the **next node**.
  - In the implementation you always **maintain a reference to the head** to the linked list and **a reference to the tail** node for quick additions/removals.

- `Doubly Linked Lists`:

  - each node holds a reference to the **next and previous node**.
  - In the implementation you always **maintain a reference to the head and the tail** of the doubly linked list to do quick additions/removals from both ends of your list.

---

## Pros and Cons

|               | Pros                                        | Cons                                   |
| ------------- | ------------------------------------------- | -------------------------------------- |
| Singly Linked | Uses less memory<br> Simpler implementation | Cannot easily access previous elements |
| Doubly Linked | Can be traversed backwards                  | Takes 2x memory                        |

---

## Complexity

|                  | Singly Linked | Doubly Linked |
| ---------------- | ------------- | ------------- |
| Search           | O(n)          | O(n)          |
| Insert at head   | O(1)          | O(1)          |
| Insert at tail   | O(1)          | O(1)          |
| Remove at head   | O(1)          | O(1)          |
| Remove at tail   | O(n)          | O(1)          |
| Remove in middle | O(n)          | O(n)          |

---

[TOP](#data-structure---array)
