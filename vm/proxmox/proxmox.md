# Proxmox

- [Installation](./install/install.md)
- [Virtual Machine](./vm/vm.md)
- [Container](./container/container.md)
- [Backup and Snapshot](./bkp_snap/bkp_snap.md)
- [CLI](./cli/cli.md)

---

- Hands-on

- [Virtualizing pfSense](./pro/pfsense/pfsense.md)

---

```sh
apt install pve-esxi-import-tools -y
# pve-esxi-import-tools is already the newest version (0.7.3).


tar -xvf OL8-General.ova


qm importovf 300  OL8-General-disk1.ovf local-lvm --format raw
# can remove the ova and the files


iptables -t nat -F
iptables -F FORWARD

iptables -t nat -A POSTROUTING -s 192.168.100.1 -o wlp7s0 -j MASQUERADE
iptables -A FORWARD -s 192.168.100.1 -o wlp7s0 -j ACCEPT
iptables -A FORWARD -d 192.168.100.1 -m state --state ESTABLISHED,RELATED -i wlp7s0 -j ACCEPT
```