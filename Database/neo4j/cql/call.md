# Cypher - CALL clause

[Back](../index.md)

- [Cypher - Select Data with MATCH](#cypher---select-data-with-match)
  - [Fetch all Nodes](#fetch-all-nodes)

---

## CALL clause

- `CALL` clause

  - used to invoke a procedure deployed in the database.

- `gds`: GDS library

| Func              | Desc                          |
| ----------------- | ----------------------------- |
| `CALL gds.list()` | list the available algorithms |

- Example:

```cypher
// to project a subgraph from an existing graph
CALL gds.graph.project(
  'myGraph', // name of the graph
  'Website', // node label
  'LINKS' // relationship type
)

// Estimate PageRank scores for nodes in an existing graph
CALL gds.pageRank.write.estimate('myGraph', {
  writeProperty: 'pageRank',      // Name of the property to store PageRank scores
  maxIterations: 20,              // Maximum number of iterations for the PageRank algorithm
  dampingFactor: 0.85             // Damping factor for the PageRank algorithm
})
YIELD nodeCount,                  // Number of nodes in the graph
      relationshipCount,          // Number of relationships in the graph
      bytesMin,                   // Estimated minimum memory required
      bytesMax,                   // Estimated maximum memory required
      requiredMemory              // Estimated required memory
//╒═════════╤═════════════════╤════════╤════════╤══════════════╕
//│nodeCount│relationshipCount│bytesMin│bytesMax│requiredMemory│
//╞═════════╪═════════════════╪════════╪════════╪══════════════╡
//│5        │7                │952     │952     │"952 Bytes"   │
//└─────────┴─────────────────┴────────┴────────┴──────────────┘

// Calculate PageRank scores for nodes in an existing graph and stream the results
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
╒════════════════╤═══════════════════╕
│name            │score              │
╞════════════════╪═══════════════════╡
│"Google"        │2.0295066657310854 │
├────────────────┼───────────────────┤
│"Bing"          │1.0038222772745389 │
├────────────────┼───────────────────┤
│"Yahoo"         │1.0038222772745389 │
├────────────────┼───────────────────┤
│"Stack Overflow"│0.43442582593891277│
├────────────────┼───────────────────┤
│"GitHub"        │0.33462529835835175│
└────────────────┴───────────────────┘


// Calculate PageRank statistics for an existing graph
CALL gds.pageRank.stats('myGraph', {
  maxIterations: 20,          // Maximum number of iterations for the PageRank algorithm
  dampingFactor: 0.85         // Damping factor for the PageRank algorithm
})
YIELD centralityDistribution
RETURN centralityDistribution.max AS max
╒═════════════════╕
│max              │
╞═════════════════╡
│2.029508590698242│
└─────────────────┘


略

```
