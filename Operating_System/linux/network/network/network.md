# Linux - Network

[Back](../../index.md)

---

- [Linux - Network](#linux---network)
  - [Network](#network)
  - [Tranfer File over the network](#tranfer-file-over-the-network)
    - [Example: Upload and download file using `STFP`](#example-upload-and-download-file-using-stfp)
    - [Example: Upload file using `STFP`](#example-upload-file-using-stfp)

---

## Network

## Tranfer File over the network

- Methods

  - `SCP` - Secure copy
  - `SFTP` - SSH file transfer protocol

- CLI Client

  - `scp`
  - `sftp`
  - PuTTY Secure Copy client: `pscp.exe`
  - PuTTY Secure File Transfer client: `psftp.exe`

- GUI Client

  - Cyberduck
  - FileZilla
  - WinSCP

- `ftp`:
  - a protocol but no secury
  - unencrypted, credentials are sent in plain text.

---

| Command                  | Desc                            |
| ------------------------ | ------------------------------- |
| `scp source destination` | Copy source to destination.     |
| `sftp host`              | Start a sftp session with host. |
| `sftp jason@host`        | Start a sftp session with host. |

---

### Example: Upload and download file using `STFP`

```sh
# create a sftp session with remote instance
sftp user@ip

# upload file to remote
# return local temp directory
lpwd
# list files at the local temp
lls
# upload a local file to the remote instance
put filename
# verify by checking the remote directory
ls
# remove the uploaded file
rm filename
# verify deletion
ls -l

# Download file from remote
# create a dir locally
lmkdir local_dir
ls -l
# download file
get file local_dir
ls -l local_dir

# quit
exit
```

---

### Example: Upload file using `STFP`

```sh
scp local_file user@ip:~
```
