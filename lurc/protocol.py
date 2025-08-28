# protocol.py

class Command:
    def __init__(self, name, length, variable_length, func):
        self.name = name
        self.length = length
        self.variable_length = variable_length
        self.func = func

    def __call__(self, payload):
        return self.func(payload)


COMMANDS = {}


def CMD(name, length, variable_length=False):
    """Decorator to register a command by name."""
    def wrap(func):
        COMMANDS[name] = Command(name, length, variable_length, func)
        return func
    return wrap


def get_command(name):
    return COMMANDS.get(name)
