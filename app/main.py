import sys
import os
import subprocess

def getFirstWordEndIndex(command):
        index = command.find(" ")
        index = index + 1
        return index

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
        index = getFirstWordEndIndex(command)
        if (index == 0):
            index = len(command)
        if (command == "exit"):
            break
        elif ("echo" in command[:index]):
            if (index != 0):
                print(command[index:])
            else:
                print("")
        elif ("type" in command[:index]):
            if (command[index:] in builtinCommands):
                print(f"{command[index:]} is a shell builtin")
            else:
                command = command[index:] 
                found, path = getExecutablePath(command)
                if (found):
                    print(f"{command} is {path}")
                else:
                    print(f"{command}: not found")
        elif (command == "pwd"):
            print(os.getcwd())
        elif ("cd" in command[:index]):
            path = command[index:]
            if (path == "~"):
                path = os.environ.get('HOME')
            if (os.path.exists(path)):
                os.chdir(path)
            else:
                print(f"{command[:index - 1]}: {path}: No such file or directory")
        else:
            index = index - 1
            found, path = getExecutablePath(command[:index])
            if (found):
                subprocess.run(command, shell=True)
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
