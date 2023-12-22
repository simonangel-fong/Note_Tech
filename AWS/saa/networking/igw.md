# AWS - Internet Gateway (IGW)

[Back](../index.md)

- [AWS - Internet Gateway (IGW)](#aws---internet-gateway-igw)
  - [`Internet Gateway (IGW)`](#internet-gateway-igw)
    - [Hands-on](#hands-on)

---

## `Internet Gateway (IGW)`

- no charge
- Allows resources (e.g., `EC2 instances`) in a `VPC` connect to the Internet
- It scales **horizontally** and is highly **available** and **redundant**
- Must be **created separately from** a `VPC`
- **One** `VPC` can **only** be attached to **one** `IGW` and vice versa 一对一
- Internet Gateways _on their own_ **do not allow** Internet access…
- `Route tables` **must** also be edited!

![route_table_diagram](./pic/route_table_diagram.png)

---

### Hands-on

- Create EC2 with a subnect

![igw_handson01](./pic/igw_handson01.png)

- Try to connect with ssh
  - fail due to lack of internet gateway

![igw_handson02](./pic/igw_handson02.png)

- Create a gateway

![igw_handson04](./pic/igw_handson03.png)

![igw_handson04](./pic/igw_handson04.png)

- Attatch to a VPC

![igw_handson04](./pic/igw_handson05.png)

![igw_handson04](./pic/igw_handson06.png)

- Create Route Table
  - 1 Public
  - 1 Private

![igw_handson04](./pic/igw_handson07.png)

![igw_handson04](./pic/igw_handson08.png)

![igw_handson04](./pic/igw_handson09.png)

![igw_handson04](./pic/igw_handson10.png)

- Associate to subnects

![igw_handson04](./pic/igw_handson11.png)

![igw_handson04](./pic/igw_handson12.png)

![igw_handson04](./pic/igw_handson13.png)

![igw_handson04](./pic/igw_handson14.png)

![igw_handson04](./pic/igw_handson15.png)

- Edit route
  - if the ip matching the first, route to local
  - `0.0.0.0/0` => **all IPs**,
    - if not match the first route, route to `IGW`

![igw_handson04](./pic/igw_handson16.png)

- Result
  - Gateway + Route table = access to internet

![igw_handson04](./pic/igw_handson17.png)

---

[TOP](#aws---internet-gateway-igw)
