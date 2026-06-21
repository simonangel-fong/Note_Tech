- Common Services
  - `Virtual Networking` / `VNets`

- `Network Security Group` / `NSG`
  - `access control list(ACL)` that **controls traffic inbound and outbound** from a `subnet`.
  - layer 3 and 4
  - rule components:
    - source IP
    - source port
    - destination IP
    - destination port
    - protocol

- `Azure Virtual Network (VNet) Peering`
  - connects two or more `Azure VNets`.
  - allows resources (like Virtual Machines) in different networks to **communicate privately** through Microsoft’s private backbone network.
  - Traffic stays off the public internet, ensuring **low latency** and high bandwidth without needing extra VPN gateways or encryption.

- `Azure DNS`
  - a cloud-based `Domain Name System (DNS)` hosting and resolution service provided by Microsoft Azure.
  - translates human-readable web addresses (like example.com) into machine-readable IP addresses.
  - ~= `Amazon Route 53`

- `Azure VPN Gateway`
  - used to send encrypted traffic between `Azure Virtual Networks (VNets)`, on-premises locations, or individual devices over the public internet.

- `VPN Peering` / `site to site VPN` / `S2S`
  - connects two or more `Azure Virtual Networks (VNets)` privately using VPN
  - use case:
    - connect entire office of computers to an Azure subnet.

- `ExpressRoute`
  - a dedicated, private network service that **extends your on-premises networks** directly into the Microsoft Cloud.
  - ~= `AWS Direct Connect`
