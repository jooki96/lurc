# LURC — Lightweight Universal Remote Control

LURC is a minimal TCP protocol and Python library for sending and handling remote commands.  
It’s designed to be **lightweight**, **explicit**, and **easy to extend**.

---

## Features

- **Framed protocol**: Each message starts with a 2-byte length header.
- **Command-based**: Commands are identified by ASCII names (`"VOL"`, `"ON"`, `"MSG"`).
- **Decorator API**: Register commands on the server with `@server.CMD`.
- **Binary-safe payloads**: Payload can contain any bytes, including spaces or newlines.
- **Simple client**: Send commands from Python with `client.send_command`.

---

## Protocol Format

```
[length:2 bytes][command name ASCII][optional space][payload bytes]
```

- `length`: total number of bytes that follow.
- `command name`: ASCII string (no spaces).
- `payload`: optional raw bytes. If present, separated from the command name by a space (`0x20`).

### Examples

- `VOL 120`  
  ```
  00 05  56 4F 4C 20 78
  ```
  Command = `VOL`, Payload = `0x78` (120)

- `ON`  
  ```
  00 02  4F 4E
  ```
  Command = `ON`, no payload

- `MSG hello`  
  ```
  00 09  4D 53 47 20 68 65 6C 6C 6F
  ```
  Command = `MSG`, Payload = `"hello"`

---

## Installation

Clone the repo:

```bash
git clone https://github.com/yourname/lurc.git
cd lurc
```

Use the library in Python:

```bash
pip install -e .
```

---

## Usage

### Server

```python
from lurc import server

@server.CMD("VOL", 1)
def set_volume(data):
    print("Volume set to", data[0])
    return b"OK"

@server.CMD("ON", 0)
def turn_on(_):
    print("Turning on")
    return b"OK"

@server.CMD("MSG", 64, variable_length=True)
def message(data):
    print("Message:", data.decode())
    return b"OK"

if __name__ == "__main__":
    server.run()
```

### Client

```python
from lurc import client

print(client.send_command(("127.0.0.1", 6888), "VOL", bytes([120])))
print(client.send_command(("127.0.0.1", 6888), "ON"))
print(client.send_command(("127.0.0.1", 6888), "MSG", b"hello world"))
```

---

## License

MIT
