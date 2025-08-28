import socket

def _recv_exact(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("closed")
        buf.extend(chunk)
    return bytes(buf)

def _recv_message(sock):
    hdr = _recv_exact(sock, 2)
    size = int.from_bytes(hdr, "big")
    return _recv_exact(sock, size)

def _send_message(sock, data):
    size = len(data)
    if size > 0xFFFF:
        raise ValueError("payload too big")
    sock.sendall(size.to_bytes(2, "big") + data)

def send_command(addr, name, payload=b""):
    """
    Send a command by name with optional payload (raw bytes).
    Example:
        send_command(("127.0.0.1", 6888), "VOL", b"\x78")
        send_command(("127.0.0.1", 6888), "MSG", b"hello")
    """
    host, port = addr
    with socket.create_connection((host, port)) as sock:
        frame = name.encode("ascii")
        if payload:
            frame += b" " + payload
        _send_message(sock, frame)
        resp = _recv_message(sock)
        return resp
