import sys
import os


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
                system_path = os.environ.get('PATH')
                commandIndex = command.find(" ")
                commandIndex = commandIndex + 1
                ogcommand = command[commandIndex:] 
                command = command[commandIndex:] + ".exe"
                directories = system_path.split(":")
                found = False
                for directory in directories:
                    if os.path.exists(directory):
                        print(os.listdir(directory))
                    if os.path.exists(directory) and command in os.listdir(directory):
                        found = True
                        print(f"{ogcommand} is {directory}")
                        break
                if (not found):
                    print(f"{ogcommand}: not found")
        else:
            print(f"{command}: command not found")
