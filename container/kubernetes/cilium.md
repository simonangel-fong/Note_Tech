# K8s CNI - Cilium

[Back](./index.md)

- [K8s CNI - Cilium](#k8s-cni---cilium)
  - [BGP vs eBGP](#bgp-vs-ebgp)

---

## BGP vs eBGP

- `eBGP (External Border Gateway Protocol)`:
  - connects routers in different organizations or networks
- `iBGP (Internal Border Gateway Protocol)`:
  - connects routers within the same organization.

| Feature                 | `eBGP (External)`                                  | `iBGP (Internal)`                                    |
| ----------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| Location                | Between different Autonomous Systems (AS).         | Within the same Autonomous System (AS).              |
| Default TTL             | Set to 1 (expects peers to be directly connected). | Set to 255 (allows peers anywhere in the network).   |
| AS-PATH                 | Modifies the path by adding the local AS number.   | Leaves the AS-PATH unchanged.                        |
| Route Advertisement     | Routes learned can be sent to all peers.           | Routes learned cannot be passed to other iBGP peers. |
| Administrative Distance | Default is 20.                                     | Default is 200.                                      |
