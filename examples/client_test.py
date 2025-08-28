from lurc import client


print(client.send_command(("127.0.0.1", 6888), "VOL", bytes([120])))
print(client.send_command(("127.0.0.1", 6888), "ON"))
print(client.send_command(("127.0.0.1", 6888), "MSG", b"hello world"))
