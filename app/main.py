import sys
import os

def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    pass

def getFirstWordEndIndex(command):
        index = command.find(" ")
        index = index + 1
        return index


if __name__ == "__main__":
    while (True):
        builtinCommands = ["echo", "type", "exit"]
        main()
        command = input()
        index = getFirstWordEndIndex()
        if (command == "exit"):
            break
        elif ("echo" in command[:index]):
            print(command[index:])
        elif ("type" in command[:index]):
            if (command[index:] in builtinCommands):
                print(f"{command[index:]} is a shell builtin")
            else:
                system_path = os.environ.get('PATH')
                command = command[index:] 
                directories = system_path.split(os.pathsep)
                print(directories)
                found = False
                for directory in directories: 
                    if os.path.exists(directory) and command in os.listdir(directory):
                        found = True
                        print(f"{command} is {directory}{os.path.sep}{command}")
                        break
                if (not found):
                    print(f"{command}: not found")
        else:
            print(f"{command}: command not found")
