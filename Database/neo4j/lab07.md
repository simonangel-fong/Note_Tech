[Back](./index.md)

```cypher
// delete all
match (n)
detach
delete n

// ---------------
// Create entities

CREATE
// create email
(e1:Email{id:1,content:"email contents"}),
(e2:Email{id:2,content:"email contents"}),
(e3:Email{id:3,content:"email contents"}),
(e4:Email{id:4,content:"email contents"}),
(e5:Email{id:5,content:"email contents"}),
// create user
(charlie:User{username:"Charlie"}),
(davina:User{username:"Davina"}),
(bob:User{username:"Bob"}),
(edward:User{username:"Edward"}),
(alice:User{username:"Alice"}),
// rel: To
(e1)-[:TO]->(charlie),
(e4)-[:TO]->(davina),
(e4)-[:TO]->(bob),
(e4)-[:TO]->(edward),
(e2)-[:TO]->(davina),
(e3)-[:TO]->(bob),
(e5)-[:TO]->(alice),
// rel: cc
(e1)-[:CC]->(alice),
(e1)-[:CC]->(davina),
(e2)-[:CC]->(edward),
// rel: sent
(charlie)-[:SENT]->(e4),
(bob)-[:SENT]->(e1),
(bob)-[:SENT]->(e2),
(davina)-[:SENT]->(e3),
(davina)-[:SENT]->(e5),
// rel: bcc
(e1)-[:BCC]->(edward),
(e2)-[:BCC]->(edward),
(e5)-[:BCC]->(bob),
(e5)-[:BCC]->(edward),
// rel: allias
(alice)-[:ALLIAS_OF]->(bob)

RETURN *

```
