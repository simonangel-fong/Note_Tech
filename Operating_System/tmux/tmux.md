# Tmux

[Back](../../index.md)

- [Tmux](#tmux)
  - [Install](#install)
  - [Architecture](#architecture)
  - [Shortcut](#shortcut)
  - [Config file](#config-file)

---

## Install

```sh
sudo apt install tmux
```

---

## Architecture

3 layers

- `session`
- `window`
- `pane`

---

## Shortcut

- Session

| Command                               | Description                               |
| ------------------------------------- | ----------------------------------------- |
| `ctrl+B` +`W`                         | list Sessions and Windows                 |
| `tmux ls`                             | List all sessions                         |
| `tmux`                                | Create a new session                      |
| `tmux new -s mySession`               | Create a new session with a name          |
| `ctrl`+`B`+`D`                        | Detach the current session(running in bg) |
| `tmux a`                              | Attach the most session                   |
| `tmux a -t <session_name>`            | Attach a session with a target name       |
| `tmux kill-session`                   | Kill the most recent session.             |
| `tmux kill-session -t <session_name>` | Kill a session with a target name         |

- Window

| Command                    | Description                           |
| -------------------------- | ------------------------------------- |
| `tmux new -t mySessionWin` | Create a new session with a window    |
| `ctrl+B` +`C`              | Create a new window                   |
| `ctrl+B` +`N`              | Move the next window                  |
| `ctrl+B` +`,`              | Rename the current window             |
| `ctrl+B` +`<pane_index>`   | Set a window with the index as active |
| `ctrl+B` + `&`             | kill current windows                  |

- Pane

| Command                          | Description                         |
| -------------------------------- | ----------------------------------- |
| `ctrl+B` + `%`                   | Add a horizontal pane               |
| `ctrl+B` + `"`                   | Add a vertical pane                 |
| `ctrl+B` + `<direction>`         | Set teh active pane                 |
| `ctrl+B` + `Q`                   | Show pane index                     |
| `ctrl+B` + `Q` +`<pane_index>`   | Set a pane with the index as active |
| `ctrl+B` + `ctrl` +`<direction>` | Set pane size                       |
| `ctrl+B` + `atl + <num>`         | Set pane layout                     |
| `ctrl+B` + `x`                   | kill current pane                   |

- Copy mode and steps

| Command        | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| `ctrl+B` + `[` | Enter Copy mode                                              |
| `<space>`      | Mover cursor and press space to start and press space to end |
| `ctrl+B` + `]` | Exit Copy mode                                               |

---

## Config file

```sh
nano ~/.tmux.conf

# set -g mouse on
# setw -g mode-keys vi

# kill current server to reload
tmux kill-server
```
