"""
Usage:
  puchkidb show [option]
  puchkidb -h | --help
  puchkidb --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  puchkidb show dbs

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/triump0870/puchkidb
"""
from inspect import getmembers, isclass

from docopt import docopt

from puchkidb import __version__ as VERSION

welcome_message = """
Welcome to:
    ____             __    __   _ ____  ____
   / __ \__  _______/ /_  / /__(_) __ \/ __ )
  / /_/ / / / / ___/ __ \/ //_/ / / / / __  |
 / ____/ /_/ / /__/ / / / ,< / / /_/ / /_/ /
/_/    \__,_/\___/_/ /_/_/|_/_/_____/_____/

"""


def main():
    """Main CLI entrypoint."""
    import commands

    print (welcome_message)

    options = docopt(__doc__, version=VERSION)
    # dynamically match the command the user is trying to run with a pre-defined command class.
    for k, v in options.iteritems():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()


if __name__ == "__main__":
    main()
