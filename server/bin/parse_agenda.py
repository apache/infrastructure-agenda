#!venv/bin/python

import re

import click


@click.command()
@click.argument('file')
@click.option('--section', '-s', default=0, type=int)
def main(file, section):
    seperated_file = parse_sections(file)

    print(seperated_file[section])


def parse_sections(file_name):
    sections = []
    with open(file_name, "r") as f:
        sections.append('')
        idx = 0
        for _, line in enumerate(f):
            if re.search(r'^([ |\d]\d)\.(.*)$', line):
                sections.append(line)
                idx += 1
            else:
                sections[idx] += line

    return sections

if __name__ == "__main__":
    main()
