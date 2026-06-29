import sys, os, subprocess, shlex, readline

redirectionTypeList = ["1>", ">", "2>", ">>", "1>>", "2>>"]
builtinCommands = ["echo", "type", "exit", "pwd", "cd", "complete", "jobs", "history", "declare"]
registeredCompletionsDictionary = {}
matches = []

originalSTDOUT = sys.stdout
originalSTDERR = sys.stderr

def getAutoCompleteList():
    autoCompleteList = [command for command in builtinCommands]
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)
    executableDirectoryList = []
    for directory in directories:
        if os.path.exists(directory):
            executableDirectoryList = os.listdir(directory)
            autoCompleteList += executableDirectoryList

    return autoCompleteList


def RedirectOutput(argumentsList):
    indexOfArgumentsRemoval = -10
    isRedirectionUnsuccessful = False
    redirectionType = None

    for type in redirectionTypeList:
        try:
            indexOfArgumentsRemoval = argumentsList.index(type)
        except ValueError:
            continue
        redirectionType = type

    if redirectionType is not None:

        try:
            redirectedLocation = argumentsList[indexOfArgumentsRemoval + 1]
        except IndexError:
            print("Redirection specified but no location is provided.")
            isRedirectionUnsuccessful = True
            return isRedirectionUnsuccessful, indexOfArgumentsRemoval

        match redirectionType:
            case "2>":
                sys.stderr = open(redirectedLocation, 'w')
            case "1>" | ">":
                sys.stdout = open(redirectedLocation, 'w')
            case "1>>" | ">>":
                sys.stdout = open(redirectedLocation, 'a')
            case "2>>":
                sys.stderr = open(redirectedLocation, 'a')
            case _:
                pass
    else:
        return isRedirectionUnsuccessful, indexOfArgumentsRemoval

    return isRedirectionUnsuccessful, indexOfArgumentsRemoval

def getExecutablePath(executable):
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)
    found = False
    path = ""
    for directory in directories:
        if os.path.exists(directory) and executable in os.listdir(directory) and os.access(f"{directory}{os.path.sep}{executable}", os.X_OK):
            found = True
            path = directory + os.path.sep + executable
            return found, path
    return found, path

def getDirectory(prefix, userInput, startIndex, isUserWritingArgument):
    prefix = userInput[startIndex:] if isUserWritingArgument and len(prefix) == 0 else prefix
    backSlashIndex = userInput.rfind(os.path.sep)
    backSlashIndex = backSlashIndex if backSlashIndex != -1 else 0
    endIndex = userInput.rfind(prefix, backSlashIndex, len(userInput)) if len(prefix) > 0 and prefix != userInput[startIndex:] else len(userInput)
    directory = os.getcwd() + os.path.sep + userInput[startIndex:endIndex] if startIndex != endIndex and os.path.sep in userInput else os.getcwd()
    directory = directory[:len(directory) - 1] if directory.endswith("/") else directory
    return directory

def CompleteWord(prefix, state):
    #state is simply a counter used to identify the number of options available as well as to identify the stopping condition
    global matches
    userInput = readline.get_line_buffer()
    startIndex = userInput.find(" ")
    startIndex += 1
    doesCommandHaveCompleter = False
    command = userInput[:startIndex - 1] if startIndex != 0 and startIndex == len(userInput) else '?'
    for key in registeredCompletionsDictionary.keys():
        if key == command:
            doesCommandHaveCompleter = True

    isUserWritingArgument = bool(startIndex)
    directory = getDirectory(prefix, userInput, startIndex, isUserWritingArgument)

    if prefix == '' and not isUserWritingArgument:
        return None

    if state == 0:
        if doesCommandHaveCompleter:
            completerOutputLocation = "completerSpecificationOutut.txt"
            subprocess.run(["touch", completerOutputLocation])
            with open(completerOutputLocation, 'w+') as fileObject:
                subprocess.run([registeredCompletionsDictionary[command]], stdout=fileObject)
                matches = [line.strip("\n") + " " for line in fileObject.readlines()]
        elif isUserWritingArgument:
            documentsInCWDList = os.listdir(directory)
            documentsInCWDList = list(set(documentsInCWDList))
            matches1 = [document + os.path.sep for document in documentsInCWDList if os.path.isdir(directory + os.path.sep + document) and document.startswith(prefix)] if len(prefix) > 0 else [document + os.path.sep for document in documentsInCWDList if os.path.isdir(directory + os.path.sep + document)]
            matches2 = [document + " " for document in documentsInCWDList if not os.path.isdir(directory + os.path.sep + document) and document.startswith(prefix)] if len(prefix) > 0 else [document + " " for document in documentsInCWDList if not os.path.isdir(directory + os.path.sep + document)]
            matches = matches1 + matches2
        else:
            commands = getAutoCompleteList()
            commands = list(set(commands))
            matches = [command + " " for command in commands if command.startswith(prefix)]

    return matches[state] if state < len(matches) else None

def DisplayMatches(substitution, matches, longest_match_len):
    print()
    print("  ".join(sorted(matches)))
    sys.stdout.write("$ " + readline.get_line_buffer())
    sys.stdout.flush()


def main():
    # TODO: Uncomment the code below to pass the first stage
     completerDelimiters = readline.get_completer_delims()
     readline.set_completer_delims(completerDelimiters.replace("-", ""))
     readline.set_completer(CompleteWord)
     readline.parse_and_bind("tab: complete")
     readline.set_completion_display_matches_hook(DisplayMatches)
    

     while (True):
        sys.stdout.write("$ ")
        sys.stdout.flush()
        userInput = input()
        parsedInput = ""

        try:
            parsedInput = shlex.split(userInput)
        except ValueError:
            continue

        if not parsedInput:
            continue

        command = parsedInput[:1]
        arguments = parsedInput[1:]
        indexOfArgumentRemoval = -1

        #redirect output
        for redirectionType in redirectionTypeList:
            if redirectionType in arguments:
                isRedirectionUnsuccessful, indexOfArgumentRemoval = RedirectOutput(arguments)

                if (isRedirectionUnsuccessful):
                    continue

                arguments = arguments[:indexOfArgumentRemoval]

        if (command[0] == "exit"):
            break

        elif (command[0] == "echo"):
            print(' '.join(arguments) if len(arguments) > 0 else "")

        elif (command[0] == "type"):
            if (arguments[0] in builtinCommands):
                print(f"{" ".join(arguments)} is a shell builtin")
            else:
                found, path = getExecutablePath(" ".join(arguments))
                if (found):
                    print(f"{" ".join(arguments)} is {path}")
                else:
                    print(f"{" ".join(arguments)}: not found")

        elif (command[0] == "pwd"):
            print(os.getcwd())

        elif (command[0] == "cd"):
            path = " ".join(arguments)
            if (path == "~"):
                path = os.environ.get('HOME')
            if (os.path.exists(path)):
                os.chdir(path)
            else:
                print(f"{command[0]}: {path}: No such file or directory")

        elif (command[0] == "complete"):
            match arguments[0]:
                case "-p":
                    found = False
                    for registeredCompletion in registeredCompletionsDictionary.keys():
                        if arguments[1] == registeredCompletion:
                            found = True
                            print(f"complete -C '{registeredCompletionsDictionary[registeredCompletion]}' {arguments[1]}")
                    if not found:
                        print(f"complete: {arguments[1]}: no completion specification")
                case "-C":
                    registeredCompletionsDictionary[f"{arguments[2]}"] = arguments[1]
                case _:
                    print("No valid second argument")

        else:
            found, path = getExecutablePath(command[0])
            if (found):
                subprocess.run([command[0]] + arguments, executable=path, stdout=sys.stdout, stderr=sys.stderr)
            else:
                print(f"{command[0]}: command not found")

        if sys.stdout != originalSTDOUT:
            sys.stdout = originalSTDOUT

        if sys.stderr != originalSTDERR:
            sys.stderr = originalSTDERR


if __name__ == "__main__":
    main()