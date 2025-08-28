import socket, threading
from protocol import CMD, get_command

# ---------- Utilities ----------
def _recv_exact(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("closed")
        buf.extend(chunk)
    return bytes(buf)

def _recv_message(sock):
    # 2-byte length prefix
    hdr = _recv_exact(sock, 2)
    size = int.from_bytes(hdr, "big")
    data = _recv_exact(sock, size)
    return data

def _send_message(sock, payload):
    size = len(payload)
    if size > 0xFFFF:
        raise ValueError("payload too big")
    sock.sendall(size.to_bytes(2, "big") + payload)

# ---------- Dispatcher ----------
def _handle_command(data):
    try:
        # split into name and payload at first space
        if b" " in data:
            name, payload = data.split(b" ", 1)
        else:
            name, payload = data, b""

        name = name.decode("ascii")
        cmd = get_command(name)
        if not cmd:
            return b"ERR unknown"

        if not cmd.variable_length and len(payload) != cmd.length:
            return b"ERR wrong size"
        if cmd.variable_length and len(payload) > cmd.length:
            return b"ERR too long"

        return cmd(payload) or b""
    except Exception as e:
        return f"ERR {e}".encode()

def _handle_conn(conn):
    with conn:
        try:
            while True:
                data = _recv_message(conn)
                out = _handle_command(data)
                _send_message(conn, out)
        except ConnectionError:
            return

# ---------- Public API ----------
def run(host="127.0.0.1", port=6888):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[server] listening on {host}:{port}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=_handle_conn, args=(conn,), daemon=True).start()
