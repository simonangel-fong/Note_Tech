# Linux - Network: SCP

[Back](../../index.md)

- [Linux - Network: SCP](#linux---network-scp)
  - [SCP](#scp)
    - [Command](#command)
  - [Lab: Transfer File vis `SCP`](#lab-transfer-file-vis-scp)

---

## SCP

- `scp(Secure Copy Protocol)`

  - a protocol used to securely copy files between a local and a remote host or between two remote hosts.
  - uses `SSH (Secure Shell)` for data transfer and provides encryption to ensure the confidentiality and integrity of the data being transferred.

- Port: `22`

- Package `openssh`

---

### Command

| Command                                               | Description                                         |
| ----------------------------------------------------- | --------------------------------------------------- |
| `scp local_file user@remote_host:/path/`              | Copy a File from Local to Remote                    |
| `scp -i key_file local_file user@remote_host:/path/`  | Use a specific private key file for authentication. |
| `scp -P pnum local_file user@remote_host:/path/`      | Specify a Port                                      |
| `scp -l 500 localfile user@server:/path/`             | Limit Bandwidth                                     |
| `scp -C gz_file username@remote_host:/path/`          | Enable compression                                  |
| `scp -r /local/dir user@remote_host:/path/`           | Copy a Directory                                    |
| `scp user1@server1:/remote/file user2@server2:/path/` | Copy a File Between Two Remote Hosts                |
| `scp user@remote_host:/remote/file /local/path/`      | Copy a File from Remote to Local                    |

---

## Lab: Transfer File vis `SCP`

- Model:

  - Client-Server

- Client(RHEL8): rheladmin user
- Server(RHEL8): scpuser user

```sh
# create file on the client
su - rheladmin

touch /home/rheladmin/scp_file
echo "This is a scp file from client." > /home/rheladmin/scp_file
cat /home/rheladmin/scp_file
ll /home/rheladmin/scp_file
# -rw-rw-r--. 1 rheladmin rheladmin 32 Dec  7 15:44 /home/rheladmin/scp_file

# transfer file
scp /home/rheladmin/scp_file scpuser@192.168.204.153:/home/scpuser/
# scp_file                                      100%   32    10.6KB/s   00:00

```
