# Linux - Network: STFP

[Back](../../index.md)

- [Linux - Network: STFP](#linux---network-stfp)
  - [SFTP Protocol](#sftp-protocol)
    - [FTP vs SFTP](#ftp-vs-sftp)
  - [Package and Commands](#package-and-commands)
  - [Lab: Upload and download file using `STFP`](#lab-upload-and-download-file-using-stfp)

---

## SFTP Protocol

- `SFTP (Secure File Transfer Protocol)`

  - a secure way to transfer files over a network, integrated with the `SSH (Secure Shell)` protocol.
  - Unlike traditional FTP, `SFTP` **encrypts** both the commands and the data, ensuring security during file transfer.

- default port: `22`

- Features
  - **Based on SSH**:
    - SFTP operates over SSH, using the same port 22.
  - **Encrypted Communication**:
    - Provides confidentiality and data integrity through encryption.
  - **Secure File Management**:
    - Allows file transfers, directory listing, and file manipulations securely.
  - **Single Connection**:
    - Unlike FTP, SFTP uses only one connection for commands and data transfer.

---

### FTP vs SFTP

| Feature      | FTP                  | SFTP                         |
| ------------ | -------------------- | ---------------------------- |
| Protocol     | Unencrypted (TCP)    | Encrypted (over SSH)         |
| Default Port | 21                   | 22                           |
| Security     | No encryption        | Encrypted commands and data  |
| Connection   | Multiple connections | Single connection (over SSH) |

---

## Package and Commands

- Package: `openssh`

- Session Commands

| Command                                      | Desc                                                   |
| -------------------------------------------- | ------------------------------------------------------ |
| `sftp`                                       | Start a sftp session to a local session.               |
| `sftp host`                                  | Start a sftp session.                                  |
| `sftp username@remote_host`                  | Start a sftp session with username.                    |
| `sftp -P port username@remote_host`          | Specify the SSH port                                   |
| `sftp -i identity_file username@remote_host` | Specify a private key file for authentication          |
| `sftp -o option=value username@remote_host`  | Pass SSH options                                       |
| `sftp -b batchfile username@remote_host`     | Use a batch file for non-interactive file transfers.   |
| `sftp -C username@remote_host`               | Enable compression for faster transfer of large files. |
| `exit`/`bye`                                 | Exit the SFTP session.                                 |

- Local Command

| Command           | Description                                                     |
| ----------------- | --------------------------------------------------------------- |
| `lpwd`            | Display the current working directory on the local machine.     |
| `lls /local/dir`  | List files in the current directory on the local machine.       |
| `lcd /local/dir`  | Change the working directory on the local machine.              |
| `lmkdir dir_name` | Create new directory on the local machine.                      |
| `!`               | Switch back to local terminal, coming back to session by `exit` |
| `!command`        | Execute a shell command on the local machine (e.g., `!clear`).  |

- Remote Commands

| Command              | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `pwd`                | Display the current working directory on the remote server. |
| `ls`                 | List files on the remote server.                            |
| `cd`                 | Change directory on the remote server.                      |
| `mkdir dir_name`     | Create a directory on the remote server.                    |
| `rmdir dir_name`     | Remove a directory on the remote server.                    |
| `rename remote_file` | Rename a file on the remote server.                         |
| `rm file_name`       | Delete a file on the remote server.                         |

- Transfer Commands

| Command                        | Description                                                                       |
| ------------------------------ | --------------------------------------------------------------------------------- |
| `put local_file`               | Upload a file to the remote server.                                               |
| `put /local/file /remote/dir/` | **Upload** a file from the local machine to the remote server.                    |
| `mput /local/* /remote/dir/`   | **Upload multiple** files to the remote server (use wildcards).                   |
| `get remote_file`              | Download a file from the remote server.                                           |
| `get /remote/file /local/dir/` | **Download** a file from the remote server to the local machine.                  |
| `mget /remote/* /local/dir/`   | **Download multiple files** from the remote server (use wildcards, e.g., \*.txt). |

---

## Lab: Upload and download file using `STFP`

```sh
# create a sftp session with remote instance
sftp rheladmin@192.168.204.153
# rheladmin@192.168.204.153's password:
# Connected to 192.168.204.153.

# Navigate locally
lmkdir client_dir
lcd client_dir
lpwd
# Local working directory: /home/rheladmin/client_dir
lls
# sftp_file

# create a local file
!touch sftp_file
!echo "this is client file" > sftp_file
!cat sftp_file
# this is client file

# Navigate remotely
mkdir server_dir
cd server_dir
pwd
# Remote working directory: /home/rheladmin/server_dir
ls

# upload file to remote
put sftp_file
# Uploading sftp_file to /home/rheladmin/server_dir/sftp_file
# sftp_file                                     100%   20     7.7KB/s   00:00

# confirm
ls
# server_file

# rename file
rename sftp_file server_file
ls
# server_file

# download file
get server_file
# get server_file
# Fetching /home/rheladmin/server_dir/server_file to server_file
# /home/rheladmin/server_dir/server_file        100%   20     5.0KB/s   00:00

# confirm
lls
# server_file  sftp_file

# exit session
exit
```

---

[TOP](#linux---network-stfp)
