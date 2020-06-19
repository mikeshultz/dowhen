def echo(string):
    print(string)


CATALOG = {
    "echo": {"name": "Echo", "description": echo.__doc__, "func": echo, "stacks": [],},
}
