import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    pass


if __name__ == "__main__":
    while (True):
        builtinCommands = ["echo", "type", "exit"]
        main()
        command = input()
        if (command == "exit"):
            break
        elif ("echo" in command[:len("echo")]):
            index = command.find(" ")
            index = index + 1
            print(command[index:])
        elif ("type" in command[:len("type")]):
            index = command.find(" ")
            index = index + 1
            if (command[index:] in builtinCommands):
                print(f"{command[index:]} is a shell builtin")
            else:
                print(f"{command[index:]}: not found")
        else:
            print(f"{command}: command not found")
