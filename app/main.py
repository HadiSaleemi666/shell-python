import sys
import os
import subprocess

def getCommandAndArguementIndexes(command):
        index = command.find(" ")
        index = index + 1
        if (index == 0):
            return len(command), -1
        return index - 1, index

def getExecutablePath(command):
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)
    found = False
    path = ""
    for directory in directories: 
        if os.path.exists(directory) and command in os.listdir(directory) and os.access(f"{directory}{os.path.sep}{command}", os.X_OK):
            found = True
            path = directory + os.path.sep + command
            return found, path
    return found, path

def main():
    # TODO: Uncomment the code below to pass the first stage
     builtinCommands = ["echo", "type", "exit", "pwd"]
     while (True):
        sys.stdout.write("$ ")
        command = input()
        endOfCommand, startOfArguements = getCommandAndArguementIndexes(command)
        if (command == "exit"):
            break
        elif ("echo" in command[:endOfCommand]):
            if (startOfArguements != -1):    
                command = command[startOfArguements:]
                if ("'" not in command):
                    command = command.split()
                    command = " ".join(command)
                else:
                    command = command.split("'")
                    command = "".join(command)
                print(command)
            else:
                print("")
        elif ("type" in command[:endOfCommand]):
            if (command[startOfArguements:] in builtinCommands):
                print(f"{command[startOfArguements:]} is a shell builtin")
            else:
                command = command[startOfArguements:] 
                found, path = getExecutablePath(command)
                if (found):
                    print(f"{command} is {path}")
                else:
                    print(f"{command}: not found")
        elif (command == "pwd"):
            print(os.getcwd())
        elif ("cd" in command[:endOfCommand]):
            path = command[startOfArguements:] if startOfArguements != -1 else ""
            if (path == "~"):
                path = os.environ.get('HOME')
            if (os.path.exists(path)):
                os.chdir(path)
            else:
                print(f"{command[:endOfCommand]}: {path}: No such file or directory")
        else:
            found, path = getExecutablePath(command[:endOfCommand])
            if (found):
                subprocess.run(command, shell=True)
            else:
                print(f"{command[:endOfCommand]}: command not found")


if __name__ == "__main__":
    main()
