import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    pass


if __name__ == "__main__":
    while (True):
        main()
        command = input()
        if (command == "exit"):
            break
        elif ("echo" in command):
            print(command[len("echo") + 1:])
        else:
            print(f"{command}: command not found")
