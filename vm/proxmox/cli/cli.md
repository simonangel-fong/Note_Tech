# Proxmox - Command Line Interface

[Back](../proxmox.md)

- [Proxmox - Command Line Interface](#proxmox---command-line-interface)
  - [VM CLI: `qm`](#vm-cli-qm)
    - [Creation CLI Template](#creation-cli-template)
  - [Container CLI: `qm`](#container-cli-qm)
    - [Container Setup Template](#container-setup-template)

---

## VM CLI: `qm`

- VM Basic Operations

| CMD                                                                          | DESC                                  |
| ---------------------------------------------------------------------------- | ------------------------------------- |
| `qm list`                                                                    | List all VMs                          |
| `qm create vm_id --name vm_name --memory MB_size --net0 virtio,bridge=vmbr0` | Create a VM (basic)                   |
| `qm destroy vm_id`                                                           | Delete VM (careful!)                  |
| `qm start vm_id`                                                             | Start VM                              |
| `qm reboot vm_id`                                                            | Reboot VM                             |
| `qm shutdown vm_id`                                                          | Graceful shutdown                     |
| `qm reset vm_id`                                                             | reste VM only when vm is stuck 硬重启 |
| `qm stop vm_id`                                                              | Force stop VM 硬关闭                  |

- VM Management

| CMD                       | DESC                                 |
| ------------------------- | ------------------------------------ |
| `qm config vm_id`         | List VM config                       |
| `qm set vm_id --onboot 1` | Modify the VM config (Start at boot) |
| `qm status vm_id`         | Show VM status                       |
| `qm terminal vm_id`       | Access VM console                    |
| `qm monitor vm_id`        | Advanced VM control (qemu monitor)   |

- Clone, Backup, Restore

| CMD                                             | DESC                   |
| ----------------------------------------------- | ---------------------- |
| `qm clone source_vmid new_vmid --name new_name` | Clone a VM             |
| `vzdump vm_id --storage storage_name`           | Backup VM              |
| `qmrestore backup_file new_vmid`                | Restore VM from backup |

---

### Creation CLI Template

```sh
# 1. Create a new empty VM
qm create 101 --name ubuntu-test --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0 --ostype l26 --scsihw virtio-scsi-pci

# 2. Attach an ISO (install image)
qm set 101 --cdrom local:iso/ubuntu-22.04.iso

# 3. Add a virtual hard disk
qm set 101 --scsi0 local-lvm:32   # 32GB disk on storage 'local-lvm'

# 4. Enable boot from ISO
qm set 101 --boot order=scsi0,cdrom

# 5. (Optional) Enable QEMU Guest Agent (if OS supports it)
qm set 101 --agent enabled=1

# 6. Start the VM
qm start 101
```

---

## Container CLI: `qm`

- Container Basic Operations

| CMD                                                                                       | DESC                   |
| ----------------------------------------------------------------------------------------- | ---------------------- |
| `pct list`                                                                                | List all containers    |
| `pct create vm_id template_path --hostname name --storage size --memory size --cores num` | Create a new container |
| `pct destroy vm_id`                                                                       | Delete container       |
| `pct start vm_id`                                                                         | Start container        |
| `pct stop vm_id`                                                                          | Stop container         |
| `pct shutdown vm_id`                                                                      | Graceful shutdown      |

- Container Management

| CMD                        | DESC                    |
| -------------------------- | ----------------------- |
| `pct config vm_id`         | Show container config   |
| `pct set vm_id --onboot 1` | Modify container config |
| `pct status vm_id`         | Show container status   |
| `pct enter vm_id`          | Enter container shell   |

- Backup, Restore, Clone

| CMD                                            | DESC                          |
| ---------------------------------------------- | ----------------------------- |
| `vzdump vm_id --storage storage_name`          | Backup container              |
| `pct restore vm_id backup_file`                | Restore container from backup |
| `pct clone vm_id new_vmid --hostname new_name` | Clone container               |

- Networking, Resources

| CMD                                                   | DESC                          |
| ----------------------------------------------------- | ----------------------------- |
| `pct set vm_id --net0 name=eth0,bridge=vmbr0,ip=dhcp` | Set networking (or static IP) |
| `pct set vm_id --memory size --cores num`             | Adjust memory and CPU         |
| `pct resize vm_id disk +size`                         | Resize disk (e.g., +10G)      |

---

### Container Setup Template

```sh
pct create 201 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
    --hostname test-container \
    --storage local-lvm \
    --memory 2048 \
    --cores 2 \
    --net0 name=eth0,bridge=vmbr0,ip=dhcp

pct start 201
```
