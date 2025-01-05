# Server - Web: Connect Homelab with `cloudflare`

[Back](../../index.md)

- [Server - Web: Connect Homelab with `cloudflare`](#server---web-connect-homelab-with-cloudflare)
  - [Homelab Server Configuration](#homelab-server-configuration)
  - [Cloudflare Configuration](#cloudflare-configuration)
    - [Update Nameserver](#update-nameserver)
    - [Create Cloudflare Tunnel](#create-cloudflare-tunnel)
    - [Disconnect Homelab](#disconnect-homelab)

---

## Homelab Server Configuration

- Parameters of homelab server

  - OS: `Oracle Linux Server 8.10`
  - Web software: `nginx`, start, enabled
  - Firewall: 80/tcp
  - Local address: `192.168.1.11`
  - Customized website: yes

- Confirm within the internal network

![local_machine01](./pic/local_machine01.png)

---

## Cloudflare Configuration

### Update Nameserver

1. With registar `AWS Route53`, register a domain `arguswatcher.net`
2. In `cloudflare`, add DNS record with the target domain name.
   - Copy the Nameservers addresses.
3. Within registar `AWS Route53`, update the nameservers.
   - Update the NS value: **`Route53`** > **Domains** > **Registered domains** > select domain name > **Details.Actions.Edit name servers**
   - **Donot** update the value in **Hosted zones**.

![domain_ns01.png](./pic/domain_ns01.png)

- Wait for a moment.
  - Status： Active

![cloudflare_dns](./pic/cloudflare_dns.png)

---

### Create Cloudflare Tunnel

- Dashboard > **Zero Trust**

![cloudflare_tunnel](./pic/cloudflare_tunnel01.png)

- Create team name and choose plan.

![cloudflare_tunnel](./pic/cloudflare_tunnel02.png)

![cloudflare_tunnel](./pic/cloudflare_tunnel03.png)
![cloudflare_tunnel](./pic/cloudflare_tunnel04.png)

- Create Tunnels

![cloudflare_tunnel](./pic/cloudflare_tunnel05.png)

![cloudflare_tunnel](./pic/cloudflare_tunnel06.png)

![cloudflare_tunnel](./pic/cloudflare_tunnel07.png)

- Copy the codes for the local machine.

![cloudflare_tunnel](./pic/cloudflare_tunnel08.png)

- Add Public hostname
  - the value of url is the ip addresses in the internal network.

![cloudflare_tunnel](./pic/cloudflare_tunnel09.png)

- Run the codes at local

![install_cloudflare](./pic/install_cloudflare01.png)

![install_cloudflare](./pic/install_cloudflare02.png)

- Confirm by accessing domain

![confirm](./pic/confirm01.png)

---

### Disconnect Homelab

- If disconnection is required, stop the cloudflare service in local machine.

![local_machine](./pic/local_machine02.png)

- Confirm disconnection

![confirm02](./pic/confirm02.png)

---

[TOP](#server---web-connect-homelab-with-cloudflare)
