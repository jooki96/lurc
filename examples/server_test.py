
from lurc import server.CMD, server.run


@CMD("VOL", 1)
def set_volume(data):
    print("Volume set to", data[0])
    return b"END"

@CMD("OFF", 0)
def turn_off(_):
    print("Turning off")
    return b"END"

@CMD("ON", 0)
def turn_on(_):
    print("Turning on")
    return b"END"

@CMD("MSG", 64, variable_length=True)
def message(data):
    print("Message:", data.decode())
    return b"END"

if __name__ == "__main__":
    run()
