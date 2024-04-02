# Data Model

[Back](../../index.md)

- [Data Model](#data-model)
  - [Property Graph Model](#property-graph-model)

---

## Property Graph Model

- `Property Graph Model`

  - the Neo4j model for storing and managing its data.

- `features`

  - The Graph model contains `Nodes`, `Relationships` and `Properties` which specifies data and its operation.
    - `Properties` are **key-value pairs**.
    - `Nodes` are represented using **circle**
    - Both `Nodes` and `Relationships` contain `properties`.
  - `Relationships` are represented using **arrow keys**.
    - Relationship specifies the relation between **two nodes**.
    - two types of relationships between nodes according to their **directions**:
      - `Unidirectional`单向
      - `Bidirectional`双向
    - Each Relationship contains two **nodes**:
      - `Start Node` / `From Node`
      - `To Node` / `End Node`

- Relationships **should be directional** in Property Graph Data Mode.不能没有方向
  - If you create a relationship without a direction, it will through an **error** message.

![Property Graph Model](./pic/Property%20Graph%20Model.png)

---

[TOP](#data-model)
