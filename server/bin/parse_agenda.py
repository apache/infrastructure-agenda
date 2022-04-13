#!../venv/bin/python
import sys
import os

import click

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import agenda


@click.command()
@click.argument('file')
def main(file):
    parsed_file = agenda.parsers.AgendaParser(file)

    print(parsed_file.orders)


if __name__ == "__main__":
    main()
