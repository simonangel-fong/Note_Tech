# Azure: Computing - VM

[Back](../index.md)

- [Azure: Computing - VM](#azure-computing---vm)
  - [Virtual Machine(VM)](#virtual-machinevm)
  - [Availability Sets](#availability-sets)
  - [Proximity Group](#proximity-group)
  - [Common Commands](#common-commands)

---

## Virtual Machine(VM)

- A `vm` must associate with **at least one** `subnet` via `NIC`

---

## Availability Sets

- `Availability Set`
  - a logical grouping of `Virtual Machines (VMs)` that distributes them across **isolated hardware and update domains**
  - By placing two or more `VMs` in a set
- **Benefits:**
  - minimize correlated failures
  - ensure resilience against physical hardware outages
  - qualify for the Azure Compute SLA of 99.95%.

- using two core mechanisms
  - `Fault Domains (FDs)`:
    - Represent the **underlying physical hardware**.
    - VMs within different FDs have separate power sources and network switches.
    - By default, Azure places VMs across up to 3 FDs.

  - `Update Domains (UDs)`:
    - Represent groups of VMs and their underlying physical hardware that can be **rebooted at the same time**.
    - During planned Azure maintenance, updates are applied one UD at a time, allowing other VMs to remain online.

---

## Proximity Group

- `Proximity Placement Group (PPG)`
  - a logical compute grouping used to **physically locate** Azure virtual machines (VMs), availability sets, and VM scale sets as close together as possible.

- Benefits:
  - minimizes **physical distance**,
  - drastically reducing **network latency** for performance-critical, multi-tiered applications

- Configuration:
  - VM > Scale Set

---

## Common Commands

- Metadata

| Command                                                      | Description                          |
| ------------------------------------------------------------ | ------------------------------------ |
| `az vm image list --output table`                            | List common VM images.               |
| `az vm image list --offer UbuntuServer --all --output table` | Search VM images by offer.           |
| `az vm list-sizes --location canadacentral -o table`         | List available VM sizes in a region. |

- VM

| Command                                                                                  | Description                                            |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `az vm create`                                                                           | Create a VM                                            |
| `az vm list`                                                                             | List VMs.                                              |
| `az vm show`                                                                             | Show full VM details.                                  |
| `az vm get-instance-view`                                                                | Show VM runtime status.                                |
| `az vm list-ip-addresses`                                                                | Show public and private IP addresses.                  |
| `az vm open-port`                                                                        | Open an inbound port.                                  |
| `az ssh vm`                                                                              | SSH into a Linux VM using Azure CLI helper.            |
| `az vm start`                                                                            | Start a stopped/deallocated VM.                        |
| `az vm stop`                                                                             | Stop the VM but keep it allocated.                     |
| `az vm deallocate`                                                                       | Stop and deallocate the VM to release compute billing. |
| `az vm restart`                                                                          | Restart the VM.                                        |
| `az vm resize`                                                                           | Change the VM size.                                    |
| `az vm update --set tags.env=dev`                                                        | Update VM properties, such as tags.                    |
| `az vm run-command invoke --command-id RunShellScript --scripts "uname -a"`              | Run a shell command inside a Linux VM.                 |
| `az vm run-command invoke --command-id RunPowerShellScript --scripts "Get-ComputerInfo"` | Run PowerShell inside a Windows VM.                    |
| `az vm extension list`                                                                   | List VM extensions.                                    |
| `az vm extension delete --name <extension-name>`                                         | Delete a VM extension.                                 |
| `az vm disk attach --name data-disk-01 --new --size-gb 32`                               | Create and attach a new data disk to a VM.             |
| `az vm disk detach --name data-disk-01`                                                  | Detach a data disk from a VM.                          |
| `az vm auto-shutdown --time 2300`                                                        | Configure VM auto-shutdown at 23:00.                   |
| `az vm auto-shutdown --off`                                                              | Disable VM auto-shutdown.                              |
| `az vm delete`                                                                           | Delete a VM.                                           |

```sh
# Create a Linux VM with SSH key authentication
az vm create                    \
  --resource-group rg-vm-demo   \
  --name vm-demo                \
  --image Ubuntu2204            \
  --size Standard_B1s           \
  --admin-username azureuser    \
  --generate-ssh-keys

# Create a Windows VM.
az vm create                    \
  --resource-group rg-vm-demo   \
  --name vm-win-demo            \
  --image Win2022Datacenter     \
  --admin-username azureuser    \
  --admin-password '<Password>'


az vm get-instance-view -g azure-study -n my-mv -o table
az vm list-ip-addresses -g azure-study -n my-mv -o table

az vm start -g azure-study -n my-mv
az vm stop -g azure-study -n my-mv
az vm restart -g azure-study -n my-mv
az vm deallocate -g azure-study -n my-mv

az vm delete -g azure-study -n my-mv
```
