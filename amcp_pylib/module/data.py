from amcp_pylib.core import Command, command_syntax


@command_syntax('DATA STORE [name:string] [data:string]')
def DATA_STORE(command: Command) -> Command:
    """
    Stores the dataset data under the name name.
    Directories will be created if they do not exist.
    """
    return command


@command_syntax('DATA RETRIEVE [name:string]')
def DATA_RETRIEVE(command: Command) -> Command:
    """
    Returns the data saved under the name name.
    """
    return command


@command_syntax('DATA LIST {[sub_directory:string]}')
def DATA_LIST(command: Command) -> Command:
    """
    Returns a list of stored datasets.
    If the optional sub_directory is specified only the datasets in that sub directory will be returned.
    """
    return command


@command_syntax('DATA REMOVE [name:string]')
def DATA_REMOVE(command: Command) -> Command:
    """
    Removes the dataset saved under the name name.
    """
    return command
